import datetime
from collections import defaultdict
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import attrs
import pendulum

from tecton_core import feature_definition_wrapper
from tecton_core import query_consts
from tecton_core import schema
from tecton_core import time_utils
from tecton_core.specs import LifetimeWindowSpec
from tecton_core.specs import OnlineBatchTablePart as SpecOnlineBatchTablePart
from tecton_core.specs import OnlineBatchTablePartTile as SpecOnlineBatchTablePartTile
from tecton_core.specs import TimeWindowSpec
from tecton_core.specs import create_time_window_spec_from_data_proto
from tecton_proto.data import feature_view__client_pb2 as feature_view__data_pb2


@attrs.frozen
class AggregationGroup:
    """AggregationGroup represents a group of aggregate features to compute with a corresponding start/end.

    The typical usage of this will be in compaction jobs, where we will use the start/end time to determine
    eligible rows for each individual aggregate. The tile index and start/end time correspond to an OnlineBatchTablePartTile for this aggregation window group. Each tile may represent a smaller time window, within the larger aggregation window, to compute futures for.
    """

    window_index: int
    inclusive_start_time: Optional[datetime.datetime]
    exclusive_end_time: datetime.datetime
    aggregate_features: Tuple[feature_view__data_pb2.AggregateFeature, ...]
    schema: schema.Schema
    tile_index: int
    window_tile_column_name: str  # 0_0 for example


def _get_inclusive_start_time_for_window(
    exclusive_end_time: datetime.datetime,
    aggregation_window: TimeWindowSpec,
    tile_window: Optional[SpecOnlineBatchTablePartTile] = None,
) -> Optional[datetime.datetime]:
    if isinstance(aggregation_window, LifetimeWindowSpec):
        return None
    window_start_time = (
        tile_window.relative_start_time_inclusive if tile_window is not None else aggregation_window.window_start
    )
    return time_utils.get_timezone_aware_datetime(exclusive_end_time + window_start_time)


def _get_exclusive_end_time_for_window(
    exclusive_end_time: datetime.datetime,
    aggregation_window: TimeWindowSpec,
    tile_window: Optional[SpecOnlineBatchTablePartTile] = None,
) -> datetime.datetime:
    if isinstance(aggregation_window, LifetimeWindowSpec):
        return time_utils.get_timezone_aware_datetime(exclusive_end_time)
    window_end_time = (
        tile_window.relative_end_time_exclusive if tile_window is not None else aggregation_window.window_end
    )
    return time_utils.get_timezone_aware_datetime(exclusive_end_time + window_end_time)


def _get_groups_for_aggregation_part(
    agg_part: SpecOnlineBatchTablePart, exclusive_end_time: datetime.datetime, aggregation_map: Dict
) -> List[AggregationGroup]:
    """Create one aggregation group for each tile in each aggregation part.

    Stream FVs with non-lifetime windows use sawtooths and have multiple tiles per part.
    Batch feature views with non-lifetime windows have one tile set per part.
    Lifetime windows do not have tiles set in their OnlineBatchTablePart, but we still add 1 agg group per part.
    """
    tiles = agg_part.tiles or [None]
    agg_group_tiles = []
    for i, tile in enumerate(tiles):
        agg_group_tiles.append(
            AggregationGroup(
                window_index=agg_part.window_index,
                inclusive_start_time=_get_inclusive_start_time_for_window(
                    exclusive_end_time, agg_part.time_window, tile
                ),
                exclusive_end_time=_get_exclusive_end_time_for_window(exclusive_end_time, agg_part.time_window, tile),
                aggregate_features=tuple(aggregation_map[agg_part.time_window]),
                schema=agg_part.schema,
                tile_index=i,
                window_tile_column_name=f"{agg_part.window_index}_{i}",
            )
        )
    return agg_group_tiles


def aggregation_groups(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper,
    exclusive_end_time: datetime.datetime,
) -> Tuple[AggregationGroup, ...]:
    aggregation_map = defaultdict(list)
    for aggregation in fdw.trailing_time_window_aggregation().features:
        aggregation_map[create_time_window_spec_from_data_proto(aggregation.time_window)].append(aggregation)

    aggregation_parts = fdw.fv_spec.online_batch_table_format.online_batch_table_parts

    if len(aggregation_parts) != len(aggregation_map):
        msg = "unexpected difference in length of the spec's online_batch_table_format and trailing_time_window_aggregation"
        raise ValueError(msg)

    agg_groups = []
    for agg_part in aggregation_parts:
        agg_groups += _get_groups_for_aggregation_part(agg_part, exclusive_end_time, aggregation_map)

    return tuple(agg_groups)


def _get_min_window_start_time(
    aggregation_groups: Tuple[AggregationGroup, ...], fdw: feature_definition_wrapper.FeatureDefinitionWrapper
) -> Optional[pendulum.DateTime]:
    contains_lifetime_agg = any(group.inclusive_start_time is None for group in aggregation_groups)
    if contains_lifetime_agg:
        return fdw.materialization_start_timestamp
    min_window_time = min(group.inclusive_start_time for group in aggregation_groups)
    return pendulum.instance(min_window_time)


def _get_max_window_end_time(aggregation_groups: Tuple[AggregationGroup, ...]) -> pendulum.DateTime:
    max_window_time = max(group.exclusive_end_time for group in aggregation_groups)
    return pendulum.instance(max_window_time)


def get_data_time_limits_for_compaction(
    fdw: feature_definition_wrapper.FeatureDefinitionWrapper, compaction_job_end_time: datetime.datetime
) -> Optional[pendulum.Period]:
    """Compute the time filter to be used for online compaction jobs.

    This determines how much data to read from the offline store.
    For aggregate fvs,
        start_time=earliest agg window start
        end_time=latest agg window end
    For non agg fvs,
        start_time=max(feature start time, compaction_job_end_time - ttl)
        end_time=compaction_job_end_time"""
    if fdw.materialization_start_timestamp is None:
        return None

    if fdw.is_temporal_aggregate:
        agg_groups = aggregation_groups(fdw=fdw, exclusive_end_time=compaction_job_end_time)
        start_time = _get_min_window_start_time(agg_groups, fdw)
        end_time = _get_max_window_end_time(agg_groups)
        return pendulum.Period(start_time, end_time)

    if not fdw.is_temporal:
        msg = "Expected fv to be of type temporal or temporal aggregate."
        raise Exception(msg)

    # respect ttl and feature start time for temporal fvs
    end_time = pendulum.instance(compaction_job_end_time)
    if fdw.serving_ttl:
        if not fdw.feature_start_timestamp:
            msg = "Expected feature start time to be set for temporal fvs when ttl is set."
            raise Exception(msg)
        job_time_minus_ttl = end_time - fdw.serving_ttl
        start_time = max(fdw.feature_start_timestamp, job_time_minus_ttl)
    elif fdw.feature_start_timestamp:
        start_time = fdw.feature_start_timestamp
    else:
        msg = "Expected ttl or feature start time to be set for temporal fvs."
        raise Exception(msg)
    return pendulum.Period(start_time, end_time)


def get_sorted_tile_column_names(agg_window_index: int, agg_groups: List[AggregationGroup]) -> List[str]:
    """Calculate the list of window_tile_column_names in ascending order for a given aggregation window index."""
    assert all(
        agg_window_index == agg_group.window_index for agg_group in agg_groups
    ), "All aggregation groups must have the same window index."
    expected_tile_indexes = set(range(len(agg_groups)))
    assert {
        agg_group.tile_index for agg_group in agg_groups
    } == expected_tile_indexes, "All aggregation groups must have unique tile indexes."

    sorted_tiles = sorted(
        agg_groups,
        key=lambda agg_group: agg_group.tile_index,
    )
    return [tile.window_tile_column_name for tile in sorted_tiles]


@attrs.frozen
class SawtoothAggregationData:
    """SawtoothAggregationData represents the batch sawtooth tiles for a Feature View.

    The typical usage of this will be in offline retrieval for Feature Views that use sawtooth aggregations (i.e. Stream Fvs with compaction enabled and non lifetime windows).
    """

    batch_sawtooth_tile_sizes: List[pendulum.Duration]

    # TODO(samantha): add support for stream tile size sawtooths.
    def contains_day_sawtooths(self) -> bool:
        return any(tile_size == pendulum.Duration(days=1) for tile_size in self.batch_sawtooth_tile_sizes)

    def contains_hour_sawtooths(self) -> bool:
        return any(tile_size == pendulum.Duration(hours=1) for tile_size in self.batch_sawtooth_tile_sizes)

    def get_anchor_time_columns(self) -> List[str]:
        anchor_time_columns = []
        if self.contains_day_sawtooths():
            anchor_time_columns.append(query_consts.anchor_time_for_day_sawtooth())
        if self.contains_hour_sawtooths():
            anchor_time_columns.append(query_consts.anchor_time_for_hour_sawtooth())
        return anchor_time_columns

    def get_identifier_partition_columns(self) -> List[str]:
        anchor_time_columns = []
        if self.contains_day_sawtooths():
            anchor_time_columns.append(query_consts.is_day_sawtooth())
        if self.contains_hour_sawtooths():
            anchor_time_columns.append(query_consts.is_hour_sawtooth())
        return anchor_time_columns

    def get_anchor_time_column_for_sawtooth_size(self, sawtooth_size: pendulum.Duration) -> str:
        sawtooth_size_to_anchor_time_map = {
            pendulum.Duration(days=1): query_consts.anchor_time_for_day_sawtooth(),
            pendulum.Duration(hours=1): query_consts.anchor_time_for_hour_sawtooth(),
        }

        if sawtooth_size not in sawtooth_size_to_anchor_time_map:
            msg = f"Invalid sawtooth size: {sawtooth_size}"
            raise ValueError(msg)
        return sawtooth_size_to_anchor_time_map[sawtooth_size]

    def get_anchor_time_to_partition_columns_map(self) -> Dict[str, str]:
        anchor_time_to_identifier_map = {}
        if self.contains_day_sawtooths():
            anchor_time_to_identifier_map[query_consts.anchor_time_for_day_sawtooth()] = query_consts.is_day_sawtooth()
        if self.contains_hour_sawtooths():
            anchor_time_to_identifier_map[query_consts.anchor_time_for_hour_sawtooth()] = (
                query_consts.is_hour_sawtooth()
            )
        return anchor_time_to_identifier_map

    def get_anchor_time_to_timedelta_map(self, use_zero_timedelta: bool = False) -> Dict[str, datetime.timedelta]:
        anchor_time_to_timedelta_map = {}
        if self.contains_day_sawtooths():
            day_duration = datetime.timedelta(seconds=0) if use_zero_timedelta else datetime.timedelta(days=1)
            anchor_time_to_timedelta_map[query_consts.anchor_time_for_day_sawtooth()] = day_duration
        if self.contains_hour_sawtooths():
            hour_duration = datetime.timedelta(seconds=0) if use_zero_timedelta else datetime.timedelta(hours=1)
            anchor_time_to_timedelta_map[query_consts.anchor_time_for_hour_sawtooth()] = hour_duration
        return anchor_time_to_timedelta_map

from datetime import datetime
from unittest import TestCase
from unittest import mock

from google.protobuf.timestamp_pb2 import Timestamp
from pytz import UTC

from tecton.cli.plan import PlanListItem
from tecton.cli.plan import PlanSummary
from tecton.cli.plan import get_plans_list_items
from tecton_proto.auth import principal__client_pb2 as principal_pb2
from tecton_proto.data import state_update__client_pb2 as state_update_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


def make_principle_basic(first_name="john", last_name="smith"):
    return principal_pb2.PrincipalBasic(
        user=principal_pb2.UserBasic(
            okta_id="okta-id",
            first_name=first_name,
            last_name=last_name,
            login_email=f"{first_name}.{last_name}@tecon.ai",
        )
    )


class BaseTestCase(TestCase):
    def mockPatch(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def setUp(self) -> None:
        self.mock_metadata_service = mock.MagicMock()
        self.mockPatch("tecton._internals.metadata_service.instance", return_value=self.mock_metadata_service)


class TestListPlan(BaseTestCase):
    maxDiff = 10000

    def test_plan_list_item_from_proto(self):
        test_date = datetime(year=2024, month=1, day=1)
        pb_test_date = Timestamp()
        pb_test_date.FromDatetime(test_date)
        self.assertEqual(pb_test_date.ToDatetime(), test_date)
        plan_list_item = PlanListItem.from_proto(
            state_update_pb2.StateUpdateEntry(
                commit_id="fake_commit",
                applied_at=pb_test_date,
                applied_by="me",
                applied_by_principal=make_principle_basic(),
                workspace="here",
                sdk_version="0.0.0",
            )
        )
        self.assertEqual(
            plan_list_item,
            PlanListItem(
                plan_id="fake_commit",
                applied_by="john.smith@tecon.ai",
                applied_at=datetime(year=2024, month=1, day=1, tzinfo=UTC),
                workspace="here",
                sdk_version="0.0.0",
            ),
        )

    def test_plan_list_items_from_proto_empty(self):
        plan_list_item = PlanListItem.from_proto(state_update_pb2.StateUpdateEntry())
        self.assertEqual(
            plan_list_item, PlanListItem(plan_id="", applied_by="", applied_at=None, workspace="", sdk_version="")
        )

    def test_get_plans_list_items(self):
        self.mock_metadata_service.GetStateUpdateLog.return_value = metadata_service_pb2.GetStateUpdateLogResponse(
            entries=[
                state_update_pb2.StateUpdateEntry(
                    commit_id="fake-commit", applied_by="me", workspace="my_workspace", sdk_version="0.0.0"
                ),
                state_update_pb2.StateUpdateEntry(
                    commit_id="fake-commit2", applied_by="you", workspace="my_workspace", sdk_version="0.0.1"
                ),
            ]
        )
        items = get_plans_list_items("my_workspace", 100)
        self.mock_metadata_service.GetStateUpdateLog.assert_called_with(
            metadata_service_pb2.GetStateUpdateLogRequest(workspace="my_workspace", limit=100)
        )
        assert items == [
            PlanListItem(
                plan_id="fake-commit",
                applied_by="me",
                applied_at=None,
                workspace="my_workspace",
                sdk_version="0.0.0",
            ),
            PlanListItem(
                plan_id="fake-commit2",
                applied_by="you",
                applied_at=None,
                workspace="my_workspace",
                sdk_version="0.0.1",
            ),
        ]

    def test_get_plans_list_items_empty(self):
        self.mock_metadata_service.GetStateUpdateLog.return_value = metadata_service_pb2.GetStateUpdateLogResponse()
        items = get_plans_list_items("my_workspace", 100)
        self.mock_metadata_service.GetStateUpdateLog.assert_called_with(
            metadata_service_pb2.GetStateUpdateLogRequest(workspace="my_workspace", limit=100)
        )
        assert items == []


class TestGetPlan(BaseTestCase):
    def test_plan_summary_from_proto_empty(self):
        plan = PlanSummary.from_proto(state_update_pb2.StateUpdatePlanSummary())
        self.assertEqual(
            plan,
            PlanSummary(
                applied=False,
                applied_by="",
                applied_at=None,
                created_by="",
                created_at=None,
                workspace="",
                sdk_version="",
            ),
        )

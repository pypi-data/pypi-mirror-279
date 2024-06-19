import datetime
from dataclasses import dataclass
from typing import Optional

import click

from tecton import tecton_context
from tecton._internals import metadata_service
from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton.cli.engine import EngineCommand
from tecton_core.id_helper import IdHelper
from tecton_core.specs.utils import get_timestamp_field_or_none
from tecton_proto.data import state_update__client_pb2 as state_update_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


def format_date(datetime: datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S %Z")


@dataclass
class PlanListItem:
    plan_id: str
    applied_by: str
    applied_at: datetime.datetime
    workspace: str
    sdk_version: str

    @classmethod
    def from_proto(cls, state_update_entry: state_update_pb2.StateUpdateEntry):
        applied_by = cli_utils.display_principal(state_update_entry.applied_by_principal, state_update_entry.applied_by)
        applied_at = get_timestamp_field_or_none(state_update_entry, "applied_at")
        return cls(
            # commit_id is called plan_id in public facing UX. Re-aliasing here.
            plan_id=state_update_entry.commit_id,
            applied_by=applied_by,
            applied_at=applied_at,
            workspace=state_update_entry.workspace,
            sdk_version=state_update_entry.sdk_version,
        )


@dataclass
class PlanSummary:
    applied_at: Optional[datetime.datetime]
    applied_by: Optional[str]
    applied: bool
    created_at: datetime.datetime
    created_by: str
    workspace: str
    sdk_version: str

    @classmethod
    def from_proto(cls, state_update_summary: state_update_pb2.StateUpdatePlanSummary):
        applied_at = get_timestamp_field_or_none(state_update_summary, "applied_at")
        applied_by = cli_utils.display_principal(
            state_update_summary.applied_by_principal, state_update_summary.applied_by
        )
        applied = bool(applied_at)
        created_at = get_timestamp_field_or_none(state_update_summary, "created_at")
        return cls(
            applied=applied,
            applied_at=applied_at,
            applied_by=applied_by,
            created_at=created_at,
            created_by=state_update_summary.created_by,
            workspace=state_update_summary.workspace,
            sdk_version=state_update_summary.sdk_version,
        )


def get_plans_list_items(workspace: str, limit: int):
    request = metadata_service_pb2.GetStateUpdateLogRequest(workspace=workspace, limit=limit)
    response = metadata_service.instance().GetStateUpdateLog(request)
    return [PlanListItem.from_proto(entry) for entry in response.entries]


def get_plan(plan_id):
    plan_id = IdHelper.from_string(plan_id)
    request = metadata_service_pb2.GetStateUpdatePlanSummaryRequest(plan_id=plan_id)
    response = metadata_service.instance().GetStateUpdatePlanSummary(request)
    return PlanSummary.from_proto(response.plan)


@click.group("plan", cls=TectonGroup)
def plan():
    """⚠️  Command has moved: Use `tecton plan create` to create a plan.\n
    Manage Tecton Plans in a Workspace"""


create = EngineCommand(
    name="create",
    apply=False,
    allows_suppress_recreates=True,
    help="Create a plan: Compare your local feature definitions with remote state and show the plan to bring them in sync.",
)


plan.add_command(create)


@plan.command(uses_workspace=True)
@click.option("--limit", default=10, type=int, help="Number of log entries to return.")
def list(limit):
    """List previous tecton plans in this workspace."""
    list_impl(limit)


def list_impl(limit):
    """Implementation of tecton plan list.
    Created as a helper-function so implementation can be shared between tecton plan list
    and tecton log for backwards compatibility in 1.1"""
    # TODO: Move implenetation into list when tecton log is removed in tecton version 1.1.0
    workspace = tecton_context.get_current_workspace()
    entries = get_plans_list_items(workspace, limit)
    table_rows = [
        (entry.plan_id, entry.applied_by, format_date(entry.applied_at), entry.sdk_version) for entry in entries
    ]
    cli_utils.display_table(["Plan Id", "Created by", "Creation Date", "SDK Version"], table_rows)


@plan.command()
@click.argument("plan-id", required=True)
def show(plan_id):
    """Show details of a Tecton Plan"""
    plan = get_plan(plan_id=plan_id)
    printer.safe_print(f"Showing current status for Plan {plan_id}")
    printer.safe_print()
    printer.safe_print(f"Created at: {format_date(plan.created_at)}")
    printer.safe_print(f"Created by: {plan.created_by}")
    printer.safe_print(f"Applied: {plan.applied}")
    if plan.applied:
        printer.safe_print(f"Applied at: {format_date(plan.applied_at)}")
        printer.safe_print(f"Applied by: {plan.applied_by}")

    # TODO: Add integration test information here

"""Resource handlers for Spot by NetApp Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListCostRecordParams, GetCostRecordParams,
    CostRecordRecord, CostRecordList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_costs", "List costs in Spot by NetApp.", action_type="read", chain_callable=True, event="spot-netapp-connector.list_costs", effects=["read:costs"], data_model=CostRecordList)
async def list_costs(ctx, params: ListCostRecordParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_costs(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("key") or r.get("uuid") or "unknown")
            rname = r.get("name") or r.get("title") or r.get("label") or rid
            items.append({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r})
        return ActionResult.success({"costs": items, "total": len(items)}, summary=f"Found {len(items)} costs.")
    except Exception as e:
        return ActionResult.error(f"Error listing costs: {e}")

@chat.function("get_costrecord", "Get details of one CostRecord in Spot by NetApp.", action_type="read", chain_callable=True, event="spot-netapp-connector.get_costrecord", effects=["read:costrecord"], data_model=CostRecordRecord)
async def get_costrecord(ctx, params: GetCostRecordParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_costrecord(params.costrecord_id)
        rid = str(r.get("id") or params.costrecord_id)
        rname = r.get("name") or r.get("title") or rid
        return ActionResult.success({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r}, summary=f"Retrieved CostRecord {rid}.")
    except Exception as e:
        return ActionResult.error(f"Error retrieving CostRecord: {e}")

@chat.function("audit_costrecord_health", "Audit health of Spot by NetApp costs and connectivity.", action_type="read", chain_callable=True, event="spot-netapp-connector.audit_costrecord_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_costrecord_health(ctx, params: ConnectionIdParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_costs(limit=50)
        return ActionResult.success({
            "healthy": True,
            "total_costs": len(items),
            "details": {"sample_count": len(items)},
            "summary": f"Spot by NetApp healthy. Sampled {len(items)} costs."
        }, summary=f"Spot by NetApp health check passed with {len(items)} costs.")
    except Exception as e:
        return ActionResult.error(f"Error auditing Spot by NetApp health: {e}")

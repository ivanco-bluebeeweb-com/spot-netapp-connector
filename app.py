"""Extension declaration, capabilities, health check for Spot by NetApp Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "spot-netapp-connector",
    version="0.1.0",
    display_name="Spot by NetApp",
    icon="icon.svg",
    capabilities=["spot_netapp:manage"],
    description="Official Imperal connector for Spot by NetApp (C30. Email Marketing & Newsletter). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("spot_netapp_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Spot by NetApp connection(s) configured." if count else "Not connected yet."
    }

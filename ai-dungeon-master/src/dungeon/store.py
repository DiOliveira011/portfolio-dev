"""In-memory campaign store (single process; resets on restart)."""

from __future__ import annotations

from dungeon.game import Campaign

_CAMPAIGNS: dict[str, Campaign] = {}


def save(campaign: Campaign) -> None:
    _CAMPAIGNS[campaign.id] = campaign


def get(campaign_id: str | None) -> Campaign | None:
    if not campaign_id:
        return None
    return _CAMPAIGNS.get(campaign_id)


def delete(campaign_id: str | None) -> None:
    if campaign_id:
        _CAMPAIGNS.pop(campaign_id, None)

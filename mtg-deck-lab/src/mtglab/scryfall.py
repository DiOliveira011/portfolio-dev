"""Scryfall client: resolve card names to normalized card data, with caching.

Uses the batched ``/cards/collection`` endpoint (up to 75 names per request) and
caches results on disk so repeated analyses are instant and gentle on the API.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests

from mtglab import normalize_name

_API = "https://api.scryfall.com/cards/collection"
_HEADERS = {"User-Agent": "mtglab/1.0", "Accept": "application/json"}
_BATCH = 75


def _chunks(seq: list, size: int):
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def _name_keys(card: dict[str, Any]) -> list[str]:
    keys = [normalize_name(card.get("name", ""))]
    for face in card.get("card_faces", []) or []:
        if face.get("name"):
            keys.append(normalize_name(face["name"]))
    return [k for k in keys if k]


def _normalize_card(card: dict[str, Any]) -> dict[str, Any]:
    faces = card.get("card_faces") or []
    image = (card.get("image_uris") or {}).get("normal")
    small = (card.get("image_uris") or {}).get("small")
    if not image and faces:
        image = (faces[0].get("image_uris") or {}).get("normal")
        small = (faces[0].get("image_uris") or {}).get("small")
    oracle = card.get("oracle_text") or " // ".join(
        f.get("oracle_text", "") for f in faces
    )
    mana_cost = card.get("mana_cost") or " // ".join(
        f.get("mana_cost", "") for f in faces
    )
    type_line = card.get("type_line", "")
    return {
        "name": card.get("name", ""),
        "cmc": float(card.get("cmc", 0) or 0),
        "mana_cost": mana_cost,
        "type_line": type_line,
        "colors": card.get("colors") or [],
        "color_identity": card.get("color_identity") or [],
        "oracle_text": oracle,
        "image": image,
        "image_small": small,
        "price_usd": (card.get("prices") or {}).get("usd"),
        "set": card.get("set", "").upper(),
        "rarity": card.get("rarity", ""),
        "is_land": "Land" in type_line,
        "is_legendary_creature": "Legendary" in type_line and "Creature" in type_line,
        "scryfall_uri": card.get("scryfall_uri", ""),
    }


def named_fuzzy(query: str) -> dict[str, Any] | None:
    """Resolve a single card by fuzzy name (used by the camera/search page)."""
    if not query or not query.strip():
        return None
    try:
        resp = requests.get(
            "https://api.scryfall.com/cards/named",
            params={"fuzzy": query.strip()},
            headers=_HEADERS,
            timeout=15,
        )
        if resp.status_code != 200:
            return None
        return _normalize_card(resp.json())
    except requests.RequestException:
        return None


class ScryfallClient:
    """Resolves card names to normalized data dictionaries."""

    def __init__(self, cache_path: str | Path | None = None) -> None:
        self._cache_path = Path(cache_path) if cache_path else None
        self._cache: dict[str, dict[str, Any]] = self._load_cache()

    def fetch(self, names: list[str]) -> tuple[dict[str, dict[str, Any]], list[str]]:
        """Return ``(resolved_by_norm_name, not_found_names)``."""
        unique = {normalize_name(n): n for n in names if n}
        index: dict[str, dict[str, Any]] = {}
        missing: list[str] = []
        needed: list[str] = []
        for norm, original in unique.items():
            if norm in self._cache:
                index[norm] = self._cache[norm]
            else:
                needed.append(original)

        for batch in _chunks(needed, _BATCH):
            identifiers = [{"name": name} for name in batch]
            try:
                resp = requests.post(
                    _API, json={"identifiers": identifiers}, headers=_HEADERS, timeout=20
                )
                resp.raise_for_status()
                payload = resp.json()
            except requests.RequestException:
                missing.extend(batch)
                continue
            for card in payload.get("data", []):
                normalized = _normalize_card(card)
                for key in _name_keys(card):
                    index[key] = normalized
                    self._cache[key] = normalized
            for nf in payload.get("not_found", []):
                if nf.get("name"):
                    missing.append(nf["name"])
            time.sleep(0.1)

        resolved: dict[str, dict[str, Any]] = {}
        for norm, original in unique.items():
            if norm in index:
                resolved[norm] = index[norm]
            elif original not in missing:
                missing.append(original)
        self._save_cache()
        return resolved, missing

    # -- cache --------------------------------------------------------------
    def _load_cache(self) -> dict[str, dict[str, Any]]:
        if self._cache_path and self._cache_path.exists():
            try:
                return json.loads(self._cache_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return {}
        return {}

    def _save_cache(self) -> None:
        if not self._cache_path:
            return
        try:
            self._cache_path.parent.mkdir(parents=True, exist_ok=True)
            self._cache_path.write_text(
                json.dumps(self._cache, ensure_ascii=False), encoding="utf-8"
            )
        except OSError:
            pass

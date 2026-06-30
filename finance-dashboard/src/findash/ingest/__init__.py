"""Statement ingestion: turn CSV/OFX files into a normalized DataFrame.

The canonical output is a pandas DataFrame with columns:
``date`` (datetime64), ``description`` (str), ``amount`` (float, signed).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from findash.ingest.csv_parser import parse_csv
from findash.ingest.ofx_parser import parse_ofx

__all__ = ["load_transactions", "parse_csv", "parse_ofx"]


def load_transactions(source: object, filename: str | None = None) -> pd.DataFrame:
    """Load a statement from a path, bytes or file-like object.

    The format is chosen from ``filename`` (or the path) extension; anything that
    isn't ``.ofx``/``.qfx`` is parsed as CSV.
    """
    name = (filename or (str(source) if isinstance(source, (str, Path)) else "")).lower()
    raw = _read(source)
    if name.endswith((".ofx", ".qfx")):
        text = raw.decode("latin-1", errors="ignore") if isinstance(raw, bytes) else raw
        return parse_ofx(text)
    return parse_csv(raw)


def _read(source: object) -> bytes | str:
    if isinstance(source, (str, Path)) and Path(source).exists():
        return Path(source).read_bytes()
    if hasattr(source, "read"):
        return source.read()  # type: ignore[no-any-return]
    if isinstance(source, (bytes, str)):
        return source
    raise TypeError(f"Unsupported source type: {type(source)!r}")

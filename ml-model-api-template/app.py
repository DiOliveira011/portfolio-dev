"""Entrypoint to run the API locally: python app.py (porta 8000)."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import uvicorn  # noqa: E402

from mlapi.api import app  # noqa: E402

if __name__ == "__main__":
    print("\n" + "=" * 56)
    print("  ML Model API Template rodando!")
    print("  API:   http://localhost:8000")
    print("  Docs:  http://localhost:8000/docs   (Swagger interativo)")
    print("=" * 56 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""Sales BI Auto-Insights — Flask app. Run: python app.py (porta 5006)."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, render_template  # noqa: E402

from salesbi import APP_TITLE, fmt_brl  # noqa: E402
from salesbi.data import generate_sales  # noqa: E402
from salesbi.insights import (  # noqa: E402
    by_dimension,
    generate_insights,
    kpis,
    monthly_series,
)

app = Flask(__name__)
app.jinja_env.globals.update(fmt_brl=fmt_brl)

DATA = generate_sales()


def _bars(mapping: dict[str, float]) -> dict:
    maximo = max(mapping.values(), default=1) or 1
    return {"itens": mapping, "max": maximo}


@app.get("/")
def index():
    series = monthly_series(DATA)
    max_mes = max((v for _, v in series), default=1) or 1
    return render_template(
        "dashboard.html", title=APP_TITLE, kpis=kpis(DATA), insights=generate_insights(DATA),
        series=series, max_mes=max_mes,
        por_categoria=_bars(by_dimension(DATA, "categoria")),
        por_regiao=_bars(by_dimension(DATA, "regiao")),
        por_canal=_bars(by_dimension(DATA, "canal")),
    )


def _lan_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


if __name__ == "__main__":
    ip = _lan_ip()
    print("\n" + "=" * 56)
    print("  Sales BI Auto-Insights rodando!")
    print("  Neste PC:   http://localhost:5006")
    print(f"  No celular: http://{ip}:5006   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5006, debug=False)

"""Text-to-SQL Analyst — Flask app. Run: python app.py (porta 5005)."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, render_template, request  # noqa: E402

from t2sql import APP_TITLE  # noqa: E402
from t2sql.nl2sql import llm_available  # noqa: E402
from t2sql.service import AnalystService  # noqa: E402

app = Flask(__name__)
svc = AnalystService()

SUGGESTIONS = [
    "Faturamento total",
    "Faturamento por mês",
    "Top produtos",
    "Vendas por região",
    "Vendas por categoria",
    "Ticket médio",
    "Melhores clientes",
    "Quantos clientes temos?",
]


def _render(question: str = "", result: dict | None = None):
    return render_template(
        "index.html", title=APP_TITLE, schema=svc.schema, stats=svc.stats(),
        suggestions=SUGGESTIONS, ia_on=llm_available(), question=question, result=result,
    )


@app.get("/")
def index():
    return _render()


@app.route("/perguntar", methods=["GET", "POST"])
def perguntar():
    question = request.values.get("q", "") or request.form.get("question", "")
    return _render(question=question, result=svc.ask(question))


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
    print("  Text-to-SQL Analyst rodando!")
    print("  Neste PC:   http://localhost:5005")
    print(f"  No celular: http://{ip}:5005   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5005, debug=False)

"""RAG Knowledge Assistant — Flask app. Run: python app.py (porta 5007)."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, render_template, request  # noqa: E402

from rag import APP_TITLE, llm  # noqa: E402
from rag.corpus import COMPANY, DOCS  # noqa: E402
from rag.service import RagService  # noqa: E402

app = Flask(__name__)
svc = RagService()

SUGGESTIONS = [
    "Quantos dias de férias eu tenho?",
    "Posso trabalhar 100% remoto?",
    "Quais são os benefícios?",
    "Como peço reembolso de uma viagem?",
    "Como abro um chamado de TI?",
    "O 2FA é obrigatório?",
]


def _render(question: str = "", result: dict | None = None):
    return render_template(
        "index.html", title=APP_TITLE, company=COMPANY, suggestions=SUGGESTIONS,
        docs=list(DOCS), provider=llm.provider_label(), ia_on=llm.available(),
        question=question, result=result,
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
    print("  RAG Knowledge Assistant rodando!")
    print(f"  IA: {llm.provider_label()}")
    print("  Neste PC:   http://localhost:5007")
    print(f"  No celular: http://{ip}:5007   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5007, debug=False)

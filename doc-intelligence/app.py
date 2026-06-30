"""Doc Intelligence — Flask app. Run: python app.py (porta 5009)."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, render_template, request  # noqa: E402

from docintel import APP_TITLE, llm  # noqa: E402
from docintel.extract import extract  # noqa: E402
from docintel.sample import SAMPLE_TEXT  # noqa: E402
from docintel.service import analyze_text, summarize  # noqa: E402

app = Flask(__name__)


def _read_doc() -> dict:
    if request.form.get("exemplo"):
        return {"kind": "texto", "text": SAMPLE_TEXT, "table": None, "warning": ""}
    file = request.files.get("arquivo")
    if file and file.filename:
        return extract(file.filename, file.read())
    text = request.form.get("texto", "").strip()
    return {"kind": "texto", "text": text, "table": None, "warning": ""}


@app.get("/")
def index():
    return render_template("index.html", title=APP_TITLE,
                           provider=llm.provider_label(), ia_on=llm.available(), result=None)


@app.post("/analisar")
def analisar():
    doc = _read_doc()
    text = doc["text"]
    result = None
    if text.strip():
        result = {
            "kind": doc["kind"], "table": doc["table"], "warning": doc["warning"],
            "analise": analyze_text(text), "resumo": summarize(text),
        }
    elif doc["warning"]:
        result = {"kind": doc["kind"], "table": None, "warning": doc["warning"],
                  "analise": None, "resumo": None}
    return render_template("index.html", title=APP_TITLE, provider=llm.provider_label(),
                           ia_on=llm.available(), result=result)


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
    print("  Doc Intelligence rodando!")
    print(f"  IA: {llm.provider_label()}")
    print("  Neste PC:   http://localhost:5009")
    print(f"  No celular: http://{ip}:5009   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5009, debug=False)

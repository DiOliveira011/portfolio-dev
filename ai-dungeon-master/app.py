"""AI Dungeon Master — Flask app. Run: python app.py (porta 5008)."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, make_response, redirect, render_template, request, url_for  # noqa: E402

from dungeon import APP_TITLE, llm, store  # noqa: E402
from dungeon.game import act, new_campaign  # noqa: E402
from dungeon.scenarios import scenario_names  # noqa: E402

app = Flask(__name__)

QUICK_ACTIONS = ["Investigar o ambiente", "Avançar com cautela", "Atacar o inimigo",
                 "Conversar", "Pegar um item", "Fugir"]


@app.get("/")
def index():
    camp = store.get(request.cookies.get("camp"))
    if camp is None:
        return render_template("start.html", title=APP_TITLE, cenarios=scenario_names(),
                               provider=llm.provider_label(), ia_on=llm.available())
    return render_template("play.html", title=APP_TITLE, camp=camp, quick=QUICK_ACTIONS,
                           provider=llm.provider_label(), ia_on=llm.available())


@app.post("/nova")
def nova():
    scenario = request.form.get("scenario", "")
    nome = request.form.get("nome", "")
    camp = new_campaign(scenario, hero_name=nome)
    store.save(camp)
    resp = make_response(redirect(url_for("index")))
    resp.set_cookie("camp", camp.id, max_age=60 * 60 * 24 * 7, samesite="Lax")
    return resp


@app.post("/acao")
def acao():
    camp = store.get(request.cookies.get("camp"))
    if camp is None:
        return redirect(url_for("index"))
    act(camp, request.form.get("action", ""))
    store.save(camp)
    return redirect(url_for("index") + "#fim")


@app.post("/encerrar")
def encerrar():
    store.delete(request.cookies.get("camp"))
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie("camp")
    return resp


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
    print("  AI Dungeon Master rodando!")
    print(f"  IA: {llm.provider_label()}")
    print("  Neste PC:   http://localhost:5008")
    print(f"  No celular: http://{ip}:5008   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5008, debug=False)

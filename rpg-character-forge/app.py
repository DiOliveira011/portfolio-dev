"""RPG Character Forge — Flask app. Run: python app.py (porta 5002)."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, redirect, render_template, request, url_for  # noqa: E402

from rpgforge.data import ABILITIES, ABILITY_NAMES, CLASSES, RACES, STANDARD_ARRAY  # noqa: E402
from rpgforge.generator import random_inputs  # noqa: E402
from rpgforge.sheet import build_character, signed  # noqa: E402
from rpgforge.store import CharacterStore  # noqa: E402

_DATA = Path(__file__).resolve().parent / "data" / "personagens.json"

app = Flask(__name__)
app.jinja_env.globals.update(
    signed=signed, ABILITIES=ABILITIES, ABILITY_NAMES=ABILITY_NAMES,
    RACES=RACES, CLASSES=CLASSES,
)
store = CharacterStore(_DATA)


def _inputs_from_form(form) -> dict:
    base = {ab: int(form.get(ab, 10) or 10) for ab in ABILITIES}
    return {
        "name": form.get("name", "").strip(),
        "race": form.get("race", "Humano"),
        "klass": form.get("klass", "Guerreiro"),
        "level": int(form.get("level", 1) or 1),
        "base_scores": base,
        "chosen_skills": form.getlist("skills") or None,
    }


def _summary(sheet: dict) -> dict:
    return {"name": sheet["name"], "race": sheet["race"], "klass": sheet["klass"],
            "level": sheet["level"]}


@app.get("/")
def index():
    defaults = dict(zip(ABILITIES, STANDARD_ARRAY, strict=False))
    return render_template("index.html", defaults=defaults, array=STANDARD_ARRAY)


@app.post("/forjar")
def forjar():
    inputs = _inputs_from_form(request.form)
    try:
        sheet = build_character(**inputs)
    except ValueError as exc:
        return render_template("index.html", defaults=inputs["base_scores"],
                               array=STANDARD_ARRAY, error=str(exc))
    return render_template("ficha.html", c=sheet, inputs=inputs, saved_id=None)


@app.get("/aleatorio")
def aleatorio():
    inputs = random_inputs()
    sheet = build_character(**inputs)
    return render_template("ficha.html", c=sheet, inputs=inputs, saved_id=None)


@app.post("/salvar")
def salvar():
    inputs = _inputs_from_form(request.form)
    sheet = build_character(**inputs)
    char_id = store.save(inputs, _summary(sheet))
    return redirect(url_for("personagem", char_id=char_id))


@app.get("/personagens")
def personagens():
    return render_template("personagens.html", chars=store.list())


@app.get("/personagem/<char_id>")
def personagem(char_id: str):
    record = store.get(char_id)
    if not record:
        return redirect(url_for("personagens"))
    sheet = build_character(**record["inputs"])
    return render_template("ficha.html", c=sheet, inputs=record["inputs"], saved_id=char_id)


@app.post("/personagem/<char_id>/excluir")
def excluir(char_id: str):
    store.delete(char_id)
    return redirect(url_for("personagens"))


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
    print("  RPG Character Forge rodando!")
    print("  Neste PC:   http://localhost:5002")
    print(f"  No celular: http://{ip}:5002   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5002, debug=False)

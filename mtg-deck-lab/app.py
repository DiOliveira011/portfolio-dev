"""MTG Deck Lab — Flask app.

Run: python app.py  (serves on 0.0.0.0:5000 — open on your phone too)
"""

from __future__ import annotations

import base64
import io
import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from dataclasses import asdict  # noqa: E402

from flask import Flask, jsonify, redirect, render_template, request, url_for  # noqa: E402

from mtglab import scryfall  # noqa: E402
from mtglab.analysis import analyze  # noqa: E402
from mtglab.decklist import parse_decklist  # noqa: E402
from mtglab.ligamagic import decklist_text_from_url  # noqa: E402
from mtglab.scryfall import ScryfallClient  # noqa: E402
from mtglab.storage import DeckStore  # noqa: E402

_DATA = Path(__file__).resolve().parent / "data"
_CACHE = _DATA / "cache" / "scryfall.json"
_DECKS = _DATA / "decks.json"

app = Flask(__name__)
store = DeckStore(_DECKS)


def _analyze_text(text: str):
    deck = parse_decklist(text)
    client = ScryfallClient(_CACHE)
    cards, missing = client.fetch(deck.names())
    return deck, analyze(deck, cards, missing=missing)


def _summary(analysis) -> dict:
    return {
        "bracket": analysis.bracket,
        "bracket_name": analysis.bracket_name,
        "colors": analysis.color_identity,
        "total": analysis.total,
        "price_brl": analysis.price_brl,
        "commander": analysis.commander["name"] if analysis.commander else None,
    }


# --------------------------------------------------------------------------- #
@app.get("/")
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze_route():
    text = (request.form.get("decklist") or "").strip()
    url = (request.form.get("url") or "").strip()
    name = (request.form.get("name") or "").strip()
    error = None
    if not text and url:
        try:
            text = decklist_text_from_url(url)
        except ValueError as exc:
            error = str(exc)
    if error or not text:
        return render_template("index.html", error=error or "Cole uma lista ou um link.")

    deck, analysis = _analyze_text(text)
    return render_template(
        "deck.html", a=analysis, rows=analysis.rows, decklist_text=text,
        deck_name=name, saved_id=None,
    )


@app.post("/save")
def save_route():
    text = (request.form.get("decklist") or "").strip()
    name = (request.form.get("name") or "").strip()
    if not text:
        return redirect(url_for("index"))
    _deck, analysis = _analyze_text(text)
    deck_id = store.save(name, text, _summary(analysis))
    return redirect(url_for("deck_route", deck_id=deck_id))


@app.get("/decks")
def decks_route():
    return render_template("decks.html", decks=store.list())


@app.get("/deck/<deck_id>")
def deck_route(deck_id: str):
    record = store.get(deck_id)
    if not record:
        return redirect(url_for("decks_route"))
    deck, analysis = _analyze_text(record["decklist"])
    return render_template(
        "deck.html", a=analysis, rows=analysis.rows, decklist_text=record["decklist"],
        deck_name=record["name"], saved_id=deck_id,
    )


@app.post("/deck/<deck_id>/delete")
def delete_route(deck_id: str):
    store.delete(deck_id)
    return redirect(url_for("decks_route"))


@app.get("/camera")
def camera_route():
    return render_template("camera.html")


@app.get("/api/search")
def api_search():
    card = scryfall.named_fuzzy(request.args.get("q", ""))
    return jsonify(_card_payload(card)) if card else (jsonify({"error": "não encontrada"}), 404)


@app.post("/recognize")
def recognize_route():
    image_bytes = _read_image(request)
    name = _ocr_card_name(image_bytes) if image_bytes else None
    if not name:
        return jsonify({"error": "Não consegui ler o nome. Digite o nome para buscar."}), 422
    card = scryfall.named_fuzzy(name)
    if not card:
        return jsonify({"error": f"Li '{name}', mas não achei a carta. Tente digitar."}), 404
    payload = _card_payload(card)
    payload["ocr"] = name
    return jsonify(payload)


# --------------------------------------------------------------------------- #
def _card_payload(card: dict) -> dict:
    return {
        "name": card["name"],
        "type_line": card["type_line"],
        "mana_cost": card["mana_cost"],
        "image": card["image"],
        "price_usd": card.get("price_usd"),
        "set": card.get("set"),
        "scryfall_uri": card.get("scryfall_uri"),
    }


def _read_image(req) -> bytes | None:
    if "image" in req.files:
        return req.files["image"].read()
    data_url = (req.form.get("image") or "").strip()
    if data_url.startswith("data:"):
        try:
            return base64.b64decode(data_url.split(",", 1)[1])
        except (ValueError, IndexError):
            return None
    return None


def _ocr_card_name(image_bytes: bytes) -> str | None:
    """OCR the card's title strip (needs pytesseract + the Tesseract binary)."""
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return None
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        width, height = img.size
        title = img.crop((0, 0, width, max(1, int(height * 0.16))))
        text = pytesseract.image_to_string(title)
    except Exception:  # noqa: BLE001 - OCR/engine not available
        return None
    for line in text.splitlines():
        cleaned = line.strip(" .,:;|")
        if len(cleaned) >= 3 and any(c.isalpha() for c in cleaned):
            return cleaned
    return None


def _lan_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


# Expose dataclass conversion to templates (mana curve etc. are plain dicts).
app.jinja_env.globals["asdict"] = asdict


if __name__ == "__main__":
    ip = _lan_ip()
    print("\n" + "=" * 56)
    print("  MTG Deck Lab rodando!")
    print("  Neste PC:   http://localhost:5000")
    print(f"  No celular: http://{ip}:5000   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=False)

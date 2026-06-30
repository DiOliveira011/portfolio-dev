"""NF-e Invoice Extractor — Flask app. Run: python app.py (porta 5003)."""

from __future__ import annotations

import csv
import io
import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, Response, render_template, request  # noqa: E402

from nfe.parser import NFeError, parse_nfe  # noqa: E402
from nfe.sample import SAMPLE_NFE_XML  # noqa: E402

app = Flask(__name__)


def _read_xml() -> str | None:
    if request.form.get("exemplo"):
        return SAMPLE_NFE_XML
    file = request.files.get("arquivo")
    if file and file.filename:
        return file.read().decode("utf-8", errors="replace")
    text = request.form.get("xml_text", "").strip()
    return text or None


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/extrair")
def extrair():
    xml = _read_xml()
    if not xml:
        return render_template("index.html", error="Envie um arquivo XML, cole o conteúdo "
                               "ou use o exemplo.")
    try:
        nfe = parse_nfe(xml)
    except NFeError as exc:
        return render_template("index.html", error=str(exc))
    return render_template("nota.html", nfe=nfe, xml=xml)


@app.get("/exemplo")
def exemplo():
    nfe = parse_nfe(SAMPLE_NFE_XML)
    return render_template("nota.html", nfe=nfe, xml=SAMPLE_NFE_XML)


@app.post("/exportar.csv")
def exportar_csv():
    xml = request.form.get("xml", "")
    nfe = parse_nfe(xml)
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";")
    writer.writerow(["codigo", "descricao", "ncm", "cfop", "quantidade",
                     "valor_unitario", "valor_total"])
    for item in nfe.itens:
        writer.writerow([item.codigo, item.descricao, item.ncm, item.cfop,
                         f"{item.quantidade:.4f}", f"{item.valor_unitario:.4f}",
                         f"{item.valor_total:.2f}"])
    csv_bytes = "﻿" + buffer.getvalue()  # BOM p/ abrir certinho no Excel
    filename = f"nfe-{nfe.numero or 'itens'}.csv"
    return Response(csv_bytes, mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename={filename}"})


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
    print("  NF-e Invoice Extractor rodando!")
    print("  Neste PC:   http://localhost:5003")
    print(f"  No celular: http://{ip}:5003   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5003, debug=False)

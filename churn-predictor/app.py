"""Churn Predictor — Flask app. Run: python app.py (porta 5004)."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, render_template, request  # noqa: E402

from churn import APP_TITLE  # noqa: E402
from churn.data import CONTRATO_ORD, CONTRATOS  # noqa: E402
from churn.service import ChurnService  # noqa: E402

app = Flask(__name__)
svc = ChurnService()


@app.get("/")
def index():
    importances = svc.importances
    max_peso = max((i["peso"] for i in importances), default=1) or 1
    return render_template(
        "cockpit.html", title=APP_TITLE, kpis=svc.kpis(), metrics=svc.metrics,
        importances=importances, max_peso=max_peso, top=svc.top_risco(25),
    )


@app.route("/simular", methods=["GET", "POST"])
def simular():
    resultado = None
    form = {"contrato": "Mensal", "tenure_meses": 6, "mensalidade": 99.9,
            "suporte_chamados": 3, "atraso_pagamento": 0, "uso_gb": 25.0}
    if request.method == "POST":
        form = {
            "contrato": request.form.get("contrato", "Mensal"),
            "tenure_meses": int(request.form.get("tenure_meses", 6) or 6),
            "mensalidade": float(request.form.get("mensalidade", 99.9) or 99.9),
            "suporte_chamados": int(request.form.get("suporte_chamados", 0) or 0),
            "atraso_pagamento": 1 if request.form.get("atraso_pagamento") else 0,
            "uso_gb": float(request.form.get("uso_gb", 25) or 25),
        }
        payload = {**form, "contrato_ord": CONTRATO_ORD[form["contrato"]]}
        resultado = svc.simulate(payload)
    return render_template("simular.html", title=APP_TITLE, contratos=CONTRATOS,
                           form=form, resultado=resultado)


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
    print("  Churn Predictor rodando!")
    print("  Neste PC:   http://localhost:5004")
    print(f"  No celular: http://{ip}:5004   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5004, debug=False)

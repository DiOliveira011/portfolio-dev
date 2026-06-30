"""Gestão de Entregas — Flask app (operação real: cadastro, baixa, SLA, auditoria).

Run: python app.py  (serve em 0.0.0.0:5001 — abre no celular também)
"""

from __future__ import annotations

import getpass
import os
import socket
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from flask import Flask, redirect, render_template, request, url_for  # noqa: E402

from gentregas import APP_TITLE, core  # noqa: E402
from gentregas.sample import RESPONSAVEIS, sample_records  # noqa: E402
from gentregas.store import EntregaStore  # noqa: E402

_DATA = Path(__file__).resolve().parent / "data" / "entregas.json"

app = Flask(__name__)
store = EntregaStore(_DATA)
store.seed_if_empty(sample_records())


def _user() -> str:
    try:
        return os.getlogin()
    except OSError:
        return getpass.getuser()


def _kpis(enriched: list[dict]) -> dict:
    entregues = [e for e in enriched if e["status_efetivo"] == "Entregue"]
    on_time = [e for e in entregues if e["no_prazo"]]
    return {
        "total": len(enriched),
        "pendentes": sum(1 for e in enriched if e["status_efetivo"] == "Pendente"),
        "em_rota": sum(1 for e in enriched if e["status_efetivo"] == "Em rota"),
        "entregues": len(entregues),
        "atrasadas": sum(1 for e in enriched if e["atrasado"]),
        "no_prazo_pct": (len(on_time) / len(entregues)) if entregues else 0.0,
        "valor_total": sum(e["valor"] for e in enriched),
        "valor_aberto": sum(e["valor"] for e in enriched if e["status_efetivo"] != "Entregue"),
    }


@app.get("/")
def index():
    status_f = request.args.get("status", "")
    resp_f = request.args.get("responsavel", "")
    q = request.args.get("q", "").strip().lower()

    enriched = [core.enrich(r) for r in store.all()]
    enriched.sort(key=lambda e: e["data_agendada"])
    kpis = _kpis(enriched)

    rows = enriched
    if status_f:
        rows = [e for e in rows if e["status_efetivo"] == status_f]
    if resp_f:
        rows = [e for e in rows if e["responsavel"] == resp_f]
    if q:
        rows = [e for e in rows if q in e["cliente"].lower() or q in e["local"].lower()]

    return render_template(
        "lista.html", rows=rows, kpis=kpis, responsaveis=RESPONSAVEIS,
        status_list=core.EFFECTIVE_STATUSES, f={"status": status_f, "responsavel": resp_f, "q": q},
        title=APP_TITLE,
    )


@app.route("/nova", methods=["GET", "POST"])
def nova():
    if request.method == "POST":
        rec = core.make(
            cliente=request.form["cliente"].strip(),
            local=request.form["local"].strip(),
            responsavel=request.form["responsavel"],
            data_agendada=request.form["data_agendada"],
            valor=request.form.get("valor", 0) or 0,
            sla_dias=request.form.get("sla_dias", core.DEFAULT_SLA) or core.DEFAULT_SLA,
            observacoes=request.form.get("observacoes", ""),
            usuario=_user(),
        )
        store.add(rec)
        return redirect(url_for("index"))
    return render_template("form.html", rec=None, responsaveis=RESPONSAVEIS,
                           statuses=core.STATUSES, title="Nova entrega")


@app.route("/editar/<entrega_id>", methods=["GET", "POST"])
def editar(entrega_id: str):
    rec = store.get(entrega_id)
    if not rec:
        return redirect(url_for("index"))
    if request.method == "POST":
        store.update(entrega_id, {
            "cliente": request.form["cliente"].strip(),
            "local": request.form["local"].strip(),
            "responsavel": request.form["responsavel"],
            "data_agendada": request.form["data_agendada"],
            "valor": float(request.form.get("valor", 0) or 0),
            "sla_dias": int(request.form.get("sla_dias", core.DEFAULT_SLA) or core.DEFAULT_SLA),
            "status": request.form.get("status", rec["status"]),
            "observacoes": request.form.get("observacoes", ""),
            "editado_por": _user(),
            "editado_em": core._now(),
        })
        return redirect(url_for("index"))
    return render_template("form.html", rec=core.enrich(rec), responsaveis=RESPONSAVEIS,
                           statuses=core.STATUSES, title="Editar entrega")


@app.post("/baixa/<entrega_id>")
def dar_baixa(entrega_id: str):
    rec = store.get(entrega_id)
    if rec:
        conferente = request.form.get("conferente", "").strip() or "—"
        core.baixa(rec, conferente, usuario=_user())
        store.update(entrega_id, rec)
    return redirect(url_for("index"))


@app.post("/excluir/<entrega_id>")
def excluir(entrega_id: str):
    store.delete(entrega_id)
    return redirect(url_for("index"))


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
    print("  Gestão de Entregas rodando!")
    print("  Neste PC:   http://localhost:5001")
    print(f"  No celular: http://{ip}:5001   (mesma rede Wi-Fi)")
    print("=" * 56 + "\n")
    app.run(host="0.0.0.0", port=5001, debug=False)

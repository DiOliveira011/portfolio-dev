"""Parse a Brazilian NF-e XML (SEFAZ layout, namespace portalfiscal)."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

NS = {"n": "http://www.portalfiscal.inf.br/nfe"}


class NFeError(ValueError):
    """Raised when the XML is not a recognizable NF-e."""


@dataclass
class Item:
    codigo: str
    descricao: str
    quantidade: float
    valor_unitario: float
    valor_total: float
    ncm: str = ""
    cfop: str = ""


@dataclass
class NFe:
    chave: str
    numero: str
    serie: str
    emissao: str
    natureza: str
    emitente: dict
    destinatario: dict
    itens: list[Item] = field(default_factory=list)
    totais: dict = field(default_factory=dict)
    validacoes: list[dict] = field(default_factory=list)

    @property
    def valido(self) -> bool:
        return all(v["ok"] for v in self.validacoes)


def _text(elem: ET.Element | None, path: str, default: str = "") -> str:
    if elem is None:
        return default
    found = elem.find(path, NS)
    return found.text.strip() if found is not None and found.text else default


def _num(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def parse_nfe(xml: str | bytes) -> NFe:
    """Parse NF-e XML → :class:`NFe` (raises :class:`NFeError` on bad input)."""
    try:
        root = ET.fromstring(xml.encode("utf-8") if isinstance(xml, str) else xml)
    except ET.ParseError as exc:  # pragma: no cover - defensive
        raise NFeError(f"XML inválido: {exc}") from exc

    inf = root.find(".//n:infNFe", NS)
    if inf is None:
        raise NFeError("Não encontrei a tag infNFe — isso não parece uma NF-e.")

    chave = (inf.get("Id") or "").removeprefix("NFe")
    ide = inf.find("n:ide", NS)
    emit = inf.find("n:emit", NS)
    dest = inf.find("n:dest", NS)

    emitente = {
        "cnpj": _text(emit, "n:CNPJ") or _text(emit, "n:CPF"),
        "nome": _text(emit, "n:xNome"),
        "municipio": _text(emit, "n:enderEmit/n:xMun"),
        "uf": _text(emit, "n:enderEmit/n:UF"),
    }
    destinatario = {
        "doc": _text(dest, "n:CNPJ") or _text(dest, "n:CPF"),
        "nome": _text(dest, "n:xNome"),
        "uf": _text(dest, "n:enderDest/n:UF"),
    }

    itens: list[Item] = []
    for det in inf.findall("n:det", NS):
        prod = det.find("n:prod", NS)
        itens.append(Item(
            codigo=_text(prod, "n:cProd"),
            descricao=_text(prod, "n:xProd"),
            quantidade=_num(_text(prod, "n:qCom")),
            valor_unitario=_num(_text(prod, "n:vUnCom")),
            valor_total=_num(_text(prod, "n:vProd")),
            ncm=_text(prod, "n:NCM"),
            cfop=_text(prod, "n:CFOP"),
        ))

    icmstot = inf.find("n:total/n:ICMSTot", NS)
    totais = {
        "produtos": _num(_text(icmstot, "n:vProd")),
        "icms": _num(_text(icmstot, "n:vICMS")),
        "pis": _num(_text(icmstot, "n:vPIS")),
        "cofins": _num(_text(icmstot, "n:vCOFINS")),
        "nota": _num(_text(icmstot, "n:vNF")),
    }

    nfe = NFe(
        chave=chave,
        numero=_text(ide, "n:nNF"),
        serie=_text(ide, "n:serie"),
        emissao=_text(ide, "n:dhEmi") or _text(ide, "n:dEmi"),
        natureza=_text(ide, "n:natOp"),
        emitente=emitente,
        destinatario=destinatario,
        itens=itens,
        totais=totais,
    )
    nfe.validacoes = _validate(nfe)
    return nfe


def _validate(nfe: NFe) -> list[dict]:
    soma_itens = round(sum(i.valor_total for i in nfe.itens), 2)
    checks = [
        ("Chave de acesso com 44 dígitos", len(nfe.chave) == 44 and nfe.chave.isdigit()),
        ("Possui ao menos um item", len(nfe.itens) > 0),
        ("Emitente identificado", bool(nfe.emitente["nome"] and nfe.emitente["cnpj"])),
        ("Destinatário identificado", bool(nfe.destinatario["nome"])),
        (
            f"Soma dos itens (R$ {soma_itens:.2f}) confere com o total de produtos "
            f"(R$ {nfe.totais['produtos']:.2f})",
            abs(soma_itens - nfe.totais["produtos"]) < 0.01,
        ),
    ]
    return [{"msg": msg, "ok": bool(ok)} for msg, ok in checks]

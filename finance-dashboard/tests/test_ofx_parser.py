"""Tests for the minimal OFX parser."""

from __future__ import annotations

from findash.ingest.ofx_parser import parse_ofx

_OFX = """
OFXHEADER:100
<OFX><BANKMSGSRSV1><STMTTRNRS><STMTRS><BANKTRANLIST>
<STMTTRN><TRNTYPE>DEBIT<DTPOSTED>20240105120000<TRNAMT>-150.00<MEMO>Supermercado</STMTTRN>
<STMTTRN><TRNTYPE>CREDIT<DTPOSTED>20240106<TRNAMT>5000.00<NAME>Salario</STMTTRN>
</BANKTRANLIST></STMTRS></STMTTRNRS></BANKMSGSRSV1></OFX>
"""


def test_parse_ofx() -> None:
    df = parse_ofx(_OFX)
    assert len(df) == 2
    assert df["amount"].tolist() == [-150.0, 5000.0]
    assert df["description"].tolist() == ["Supermercado", "Salario"]
    assert str(df["date"].dtype).startswith("datetime64")

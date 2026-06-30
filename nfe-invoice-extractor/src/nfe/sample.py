"""A realistic sample NF-e XML used by the "usar exemplo" button and tests."""

from __future__ import annotations

SAMPLE_NFE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
  <NFe>
    <infNFe Id="NFe35240614200166000187550010000000071123456780" versao="4.00">
      <ide>
        <cUF>35</cUF>
        <natOp>Venda de mercadoria</natOp>
        <mod>55</mod>
        <serie>1</serie>
        <nNF>7</nNF>
        <dhEmi>2026-06-12T10:32:00-03:00</dhEmi>
        <tpNF>1</tpNF>
      </ide>
      <emit>
        <CNPJ>14200166000187</CNPJ>
        <xNome>TGMOB Locacoes e Eventos LTDA</xNome>
        <enderEmit>
          <xLgr>Av. das Festas</xLgr>
          <nro>1200</nro>
          <xMun>Sao Paulo</xMun>
          <UF>SP</UF>
        </enderEmit>
      </emit>
      <dest>
        <CNPJ>11222333000144</CNPJ>
        <xNome>Buffet Jardins Eventos ME</xNome>
        <enderDest>
          <xMun>Sao Paulo</xMun>
          <UF>SP</UF>
        </enderDest>
      </dest>
      <det nItem="1">
        <prod>
          <cProd>A100</cProd>
          <xProd>Cadeira Tiffany Transparente</xProd>
          <NCM>94017900</NCM>
          <CFOP>5102</CFOP>
          <uCom>UN</uCom>
          <qCom>50.0000</qCom>
          <vUnCom>12.0000</vUnCom>
          <vProd>600.00</vProd>
        </prod>
      </det>
      <det nItem="2">
        <prod>
          <cProd>A200</cProd>
          <xProd>Mesa Redonda 1,5m</xProd>
          <NCM>94036000</NCM>
          <CFOP>5102</CFOP>
          <uCom>UN</uCom>
          <qCom>10.0000</qCom>
          <vUnCom>45.0000</vUnCom>
          <vProd>450.00</vProd>
        </prod>
      </det>
      <det nItem="3">
        <prod>
          <cProd>A300</cProd>
          <xProd>Toalha de Mesa Branca</xProd>
          <NCM>63026000</NCM>
          <CFOP>5102</CFOP>
          <uCom>UN</uCom>
          <qCom>50.0000</qCom>
          <vUnCom>9.0000</vUnCom>
          <vProd>450.00</vProd>
        </prod>
      </det>
      <total>
        <ICMSTot>
          <vProd>1500.00</vProd>
          <vICMS>270.00</vICMS>
          <vPIS>24.75</vPIS>
          <vCOFINS>114.00</vCOFINS>
          <vNF>1500.00</vNF>
        </ICMSTot>
      </total>
    </infNFe>
  </NFe>
</nfeProc>
"""

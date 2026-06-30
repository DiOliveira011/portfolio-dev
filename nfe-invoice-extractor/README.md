# 🧾 NF-e Invoice Extractor (Flask)  ✅

> Leitor de **NF-e (Nota Fiscal eletrônica)**: envie o **XML** e o app extrai
> **emitente, destinatário, itens, impostos e totais**, roda **validações
> automáticas** (chave de 44 dígitos, soma dos itens × total declarado…) e
> **exporta os itens em CSV**. Processamento 100% local.

**Skills:** Desenvolvimento web (Flask) · parsing de XML/dados fiscais · validação
**Stack:** Python 3.12 · Flask · `xml.etree` (biblioteca padrão) · sem dependências pesadas

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** (ou `pip install -r requirements-dev.txt` +
`python app.py`). Abre em **http://localhost:5003**. Clique em **"Usar exemplo"**
para ver uma nota já carregada — não precisa ter um XML em mãos.

## ✨ O que faz
- Aceita **upload do XML** ou **colar o conteúdo** (ou usar o **exemplo**).
- Extrai **cabeçalho** (número, série, emissão, natureza, **chave de acesso**),
  **emitente/destinatário**, **itens** (código, descrição, NCM, CFOP, qtd, valores)
  e **totais** (produtos, ICMS, PIS, COFINS, total da nota).
- **Validações** automáticas com checklist visual (✓/✕).
- **Exporta CSV** dos itens (com BOM, abre certinho no Excel).

## 🧱 Arquitetura
```
nfe-invoice-extractor/
├── app.py                 # rotas Flask (extrair, exemplo, exportar.csv)
├── src/nfe/
│   ├── parser.py          # parse + validações (NF-e, namespace SEFAZ)
│   └── sample.py          # XML de exemplo
├── templates/  static/    # UI (tema fiscal azul)
└── tests/                 # parsing, totais e validações (5 testes)
```

## 🧪 Testes
`pytest` — extrai cabeçalho/itens/totais do exemplo, confere validações e
detecta inconsistência de total.

## 🗺️ Próximos
- Suporte a lote (vários XML de uma vez) e histórico.
- Leitura de **CT-e** e exportação para Excel com várias abas.

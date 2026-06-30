# 🃏 MTG Deck Lab — Commander (Flask)  ✅

> App **web** (Flask) para analisar decks de **Magic: Commander**. Cole a **lista
> em txt** ou um **link da LigaMagic**, e ele traz **tudo**: comandante, identidade
> de cor, **bracket de poder (1–5)**, curva de mana, tipos, **Game Changers** e o
> **preço** (USD do Scryfall + estimativa em R$). Salva seus decks e tem uma
> página de **câmera** para identificar cartas — **abre no celular** também.

**Skills:** Desenvolvimento web (Flask) · APIs (Scryfall) · scraping · análise
**Stack:** Python 3.12 · Flask · requests · BeautifulSoup · Pillow · Scryfall API

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** — prepara o ambiente e sobe o app. Depois abra:
- **Neste PC:** http://localhost:5000
- **No celular:** `http://SEU-IP:5000` (o endereço aparece no terminal; precisa
  estar na **mesma Wi-Fi**).

## ✨ O que faz
- **Cadastra/analisa decks** por **lista txt** (`1 Carta`, `1x Carta`,
  `1 Carta (SET) 123`, comandante com `*CMDR*`) **ou link** (LigaMagic/sites de deck).
- **Análise Commander:** comandante, identidade de cor, **curva de mana**,
  distribuição de tipos, **tutores** e **turnos extra**.
- **Bracket (1–5)** estimado pelo sistema oficial da WotC — conta **Game Changers**,
  *mass land denial*, tutores e turnos extra, e explica o porquê.
- **Preço:** soma o USD (Scryfall) e mostra um **R$ estimado** (USD × câmbio).
- **Meus decks:** salva, lista e reabre (com re-análise atualizada).
- **📷 Câmera:** captura a carta pelo navegador do celular e identifica (OCR do
  nome via Tesseract, se instalado; senão, busca por nome — sempre funciona).

## 🧱 Arquitetura
```
mtg-deck-lab/
├── app.py                # rotas Flask
├── src/mtglab/
│   ├── decklist.py       # parser de listas (txt)
│   ├── ligamagic.py      # importa lista de um link (best-effort)
│   ├── scryfall.py       # dados das cartas (lote + cache) e busca por nome
│   ├── gamechangers.py   # lista de Game Changers (heurística de bracket)
│   ├── analysis.py       # bracket, curva, tipos, preço
│   └── storage.py        # salvar/listar decks (JSON)
├── templates/  static/   # UI responsiva (mobile)
└── tests/                # parser e análise (sem rede)
```

## 🧪 Testes
`pytest` (12 testes: parsing de listas e análise/bracket — tudo offline).

## 📝 Notas
- **Câmera/OCR:** o reconhecimento por foto usa **Tesseract** (opcional). Sem ele,
  a página ainda abre no celular e você busca a carta por nome. Para OCR real:
  instale o Tesseract e `pip install pytesseract`.
- **LigaMagic:** a leitura de preço por carta (R$) é um próximo passo; hoje o
  preço-base vem do Scryfall (USD) com estimativa em R$.

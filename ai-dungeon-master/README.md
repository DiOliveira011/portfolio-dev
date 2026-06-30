# 🐉 AI Dungeon Master (Flask)  ✅

> Um **Mestre de RPG** que narra sua aventura de fantasia e **lembra do que
> aconteceu** (memória de campanha). Escolha um cenário, dê nome ao herói e jogue
> escrevendo o que faz. Com **IA (Groq grátis ou Claude)** a história fica viva;
> **sem chave**, um Mestre offline conduz com rolagens de **d20**.

**Skills:** Engenharia de IA (chat com memória/contexto) · design de sistema · Flask
**Stack:** Python 3.12 · Flask · IA via **Groq/Claude** (urllib, sem SDK) · motor offline

## 🤖 IA opcional (Groq grátis, Claude, ou offline)
Defina **uma** variável antes de abrir: `GROQ_API_KEY` (gratuito,
https://console.groq.com) **ou** `ANTHROPIC_API_KEY` (Claude). Sem chave, o jogo
roda com o Mestre offline (narração + d20). Com as duas, use `LLM_PROVIDER`.

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** ou `pip install -r requirements-dev.txt` +
`python app.py`. Abre em **http://localhost:5008** (e no celular pela rede).

## ✨ O que faz
- **3 cenários** prontos (Masmorra do Dragão, Taverna Amaldiçoada, Floresta dos
  Sussurros) e **herói gerado** (classe, PV, inventário).
- **Memória de campanha**: o histórico recente vai como contexto para a IA manter
  a continuidade.
- **Ações livres** (escreva o que quiser) + **botões rápidos** (investigar,
  atacar, conversar, pegar, fugir).
- **Modo offline**: classifica a ação e narra o desfecho com **rolagem de d20**.

## 🧱 Arquitetura
```
ai-dungeon-master/
├── app.py                 # rotas Flask (/, /nova, /acao, /encerrar) + cookie
├── src/dungeon/
│   ├── scenarios.py       # cenários (flavor/contexto)
│   ├── character.py       # geração de herói
│   ├── engine.py          # Mestre offline (classificação + d20)
│   ├── game.py            # campanha + memória + IA quando disponível
│   ├── llm.py             # Groq / Claude / offline (via urllib)
│   └── store.py           # campanhas em memória
├── templates/  static/    # UI (tema RPG escuro/dourado)
└── tests/                 # engine, jogo e provedores (10 testes)
```

## 🧪 Testes
`pytest` — classificação de ações, narração offline, criação/turnos da campanha e
resolução de provedor (sem rede).

## 🗺️ Próximos
- Persistir campanhas em disco e permitir **continuar depois**.
- Combate com PV/dano de verdade e fichas evoluindo (XP/itens).

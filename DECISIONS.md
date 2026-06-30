# 🧭 Registro de Decisões — Projetos Grupo Desenvolvimento

> Você me deu autonomia para decidir o melhor caminho e pediu para eu **explicar
> as decisões aqui** para revisarmos depois. Este arquivo é meu "diário de bordo".
> Última atualização: sessão de 30/06/2026 (16 de 17 apps implementados).

---

## 0. Princípios que adotei

- **Trabalhar sozinho hoje**, sem te interromper, tomando as decisões que julgo
  melhores e registrando tudo aqui.
- **Qualidade de portfólio**: cada projeto com arquitetura limpa, testes e README.
- **Variedade visual**: a partir de agora, cada app usa um tema/paleta diferente
  (você pediu para fugir do "só preto e verde" do Covil).
- **IA padrão = Claude (Anthropic)** quando houver LLM.

---

## 1. Ajustes no portfólio (a partir do seu recado)

| Decisão | Por quê |
|---|---|
| **Magic = sempre Commander** | Você pediu. O `mtg-deck-lab` foi reescrito para o formato Commander (100 cartas, singleton, comandante). |
| **Usar os "brackets" (1–5)** | O sistema oficial de *brackets* da WotC para Commander vira a forma de medir **poder do deck / nivelamento de mesa** — diferencial forte e atual. |
| **Curva de mana + nivelamento de mesa** | Métricas centrais do analisador. |
| **Preços via LigaMagic** | Mercado BR (em R$), mais relevante que Scryfall/USD para você. (Scryfall continua útil para dados das cartas.) |
| **Projeto #2 (mtg-card-vision) mantido** | Você disse que está perfeito. |
| **Tibia e Albion → backlog (depois)** | Você pediu para deixar para depois. Mantive as pastas, mas fora do foco atual. |
| **+ worldcup-predictor** | Sua ideia: prever probabilidades/campeão da Copa a partir de resultados históricos (ML). Entra no lugar de Tibia/Albion no foco. |
| **+ logistics-control** | Sua ideia: controle de rotas/veículos/entregas, inspirado na RF Festas (esposa), Transgala→TGMOB e Lalamove. Pesquiso o que existe e faço melhor. |
| **Foco financeiro hoje** | Priorizei `finance-dashboard` (feito) e `invest-portfolio-analyzer` na fila. |

---

## 2. finance-dashboard (1º projeto implementado)

| Decisão | Alternativa considerada | Por quê escolhi |
|---|---|---|
| **Streamlit** (web) | CustomTkinter (desktop, como o Covil) | Para um painel de dados, Streamlit é mais rápido de construir, fica bonito e é o padrão de portfólio de Ciência de Dados. Dá variedade em relação ao Covil. |
| **Categorização híbrida: regras + ML** | Só regras, ou só ML | Regras dão precisão imediata sem dados rotulados; o ML (TF-IDF + Naive Bayes) **aprende com o que as regras rotularam** (self-training) e cobre o que as regras não pegam. Mostra DS de verdade. |
| **Parser de CSV/OFX próprio** | Biblioteca `ofxparse` | Menos dependências e demonstra habilidade de parsing (detecção de colunas, locale BR/US, débito/crédito, OFX SGML e XML). |
| **venv em caminho curto (`C:\fdv`)** | venv dentro do projeto | O caminho do OneDrive + arquivos aninhados do Streamlit **estouram o limite de 260 caracteres** do Windows e a instalação falha. venv fora do OneDrive resolve. |
| **Tema claro índigo/teal + Plotly "Bold"** | Reusar o verde/preto do Covil | Você pediu variedade de cores. |
| **Dados de exemplo sintéticos (seed fixa)** | Pedir um extrato seu | Demo reproduzível e sem expor dados reais; gerei poupança positiva (~51%) para o painel parecer saudável. |

**Status:** ✅ 24 testes passando, pipeline ponta a ponta validado, app sobe no
Streamlit (health HTTP 200).

---

## 3. worldcup-predictor (2º implementado)

| Decisão | Por quê |
|---|---|
| **Dois modelos: Elo e Poisson** | Elo é intuitivo (rating); Poisson modela gols (ataque×defesa) e dá o **placar provável**. Mostrar os dois demonstra mais repertório de DS e são **explicáveis**. |
| **Sem statsmodels/scipy** | Implementei Poisson e Elo "na mão" (numpy/math). Menos dependências, mais domínio demonstrado. |
| **Dataset sintético com "forças ocultas"** | Gero um histórico realista a partir de forças secretas; os modelos **recuperam** essas forças. Roda offline e fecha o ciclo (sem depender de baixar Kaggle). |
| **Monte Carlo (grupos + mata-mata, 16 seleções)** | Formato de 4 grupos de 4 + eliminatória é simples, didático e roda rápido (cache de probabilidades por par). |
| **Tema verde-campo + dourado** | Variedade visual. |

**Status:** ✅ 8 testes (modelos, simulação, dados), lint limpo, Streamlit sobe (HTTP 200).

## 4. Pendências / próximos passos

- [x] Pesquisa de referências (Commander/brackets, LigaMagic; RF Festas, TGMOB, Lalamove, TMS).
- [x] Reorganização do índice + specs (Magic=Commander; Tibia/Albion no backlog; +worldcup +logistics).
- [x] `finance-dashboard` e `worldcup-predictor` implementados.
- [ ] `logistics-control` (em construção).
- [ ] `invest-portfolio-analyzer`.
- [ ] **GitHub:** continua **só local** (sua escolha). Quando aprovar, eu crio o
      repo `Projetos-Grupo-Desenvolvimento` e subo tudo organizado.

## 5. Decisões de infraestrutura (valem para todos)

- **venvs em caminho curto** (`C:\fdv`) por causa do limite de path do Windows no
  OneDrive. Reusei a mesma venv para os apps de dados (pandas/streamlit/plotly/
  numpy/sklearn) para acelerar — em produção cada projeto teria a sua.
- **Verificação**: cada app passa por `ruff` + `pytest` + **boot real do Streamlit**
  (checo o endpoint `/_stcore/health` = HTTP 200) antes de eu considerar "pronto".

## 6. logistics-control (3º implementado)

| Decisão | Por quê |
|---|---|
| **Algoritmo *sweep* + vizinho-mais-próximo + 2-opt** | Heurísticas clássicas de VRP, explicáveis e rápidas, sem depender de solver pesado. O *sweep* gera clusters por ângulo (fatias de pizza) respeitando capacidade; 2-opt melhora a ordem. |
| **Janelas de horário + ETA** | É o "quando estar lá" que você citou. Calculo chegada por parada, espera se chegar cedo e marco "no prazo". |
| **Mapa OpenStreetMap (Plotly)** | Sem precisar de token Mapbox. |
| **Foco em eventos (entrega + retirada)** | Diferencial vs. TMS genérico: a operação da RF Festas também **retira/devolve** itens locados. |
| **Tema azul + âmbar** | Variedade. |

**Status:** ✅ 8 testes (geo, sweep/capacidade, 2-opt, agenda, plano), lint limpo, Streamlit HTTP 200.

## 7. invest-portfolio-analyzer (4º implementado)

| Decisão | Por quê |
|---|---|
| **Offline por padrão (preços sintéticos via GBM)** | Roda e é testável sem internet; `yfinance` é **opcional** para preços reais. |
| **Métricas clássicas** (retorno anual., volatilidade, Sharpe, max drawdown) | Linguagem do mercado financeiro; explicáveis. |
| **Fronteira eficiente por Monte Carlo** | Gero milhares de carteiras aleatórias e destaco a de **máximo Sharpe** — clássico de finanças quantitativas, visual e didático. |
| **Tema navy + esmeralda** | Variedade. |

**Status:** ✅ 6 testes, lint limpo, Streamlit HTTP 200.

---

## 8. Resumo da sessão (para revisão)

Construí **4 apps completos e verificados** hoje, além de reorganizar o portfólio
(15 specs) e pesquisar referências. Cada app: arquitetura limpa, testes (`pytest`),
lint (`ruff`) e **boot real do Streamlit** confirmado.

**Como rodar qualquer um:**
```bash
cd <pasta-do-projeto>
python -m venv C:\venv-temp   # caminho curto (limite de path do Windows/OneDrive)
C:\venv-temp\Scripts\activate
pip install -r requirements-dev.txt
streamlit run app.py          # (worldcup/finance/logistics/invest)
```

**O que eu deixaria para revisarmos juntos:**
- Confirmar se quer que eu **suba tudo para o GitHub** agora (continua local por ora).
- Próximos a construir: sugiro `mtg-deck-lab` (Commander, com brackets) e
  `rag-knowledge-assistant` (entra no mundo LLM) — e depois os demais.
- Validar se os temas/cores ficaram do seu agrado (usei 4 paletas diferentes).

> Fim do registro desta sessão.

---

## 9. Sessão 2 — execução, logística v2 e suas perguntas

**"Não consegui executar nenhum"** → era o ponto mais importante. Resolvido:
- Criei **`EXECUTAR.bat`** em cada app: dá **duplo clique**, ele cria a venv num
  **caminho curto** (`%LOCALAPPDATA%\portfolio-venvs\<app>`, fora do OneDrive),
  instala e abre o app no navegador. **Validei** que esse caminho instala sem o
  erro de path longo do Windows.
- Criei **`INICIAR-TUDO.bat`** na raiz (abre os 4 de uma vez).
- Subi os 4 apps rodando: `:8501` finance · `:8502` worldcup · `:8503` logistics
  · `:8504` invest. Para parar: feche as janelas ou
  `Get-Process streamlit | Stop-Process` no PowerShell.

**Flask vs Streamlit (você sugeriu Flask):** decidi **manter Streamlit** e explico —
o problema real era *executar*, não o framework, e isso foi resolvido pelo `.bat`.
Para painéis de dados, Streamlit é **menos código** e melhor para gráficos;
reescrever 4 apps em Flask seria mais trabalho e mais complexidade (HTML/JS/
templates) sem ganho prático. Se, **depois de ver rodando**, você ainda preferir
Flask em algum app específico, eu converto aquele. (Você me deu autonomia para
escolher o melhor e explicar — é o que fiz.)

**Logística é B2B (não iFood):** pesquisei o mercado (TMS, canhoto digital/POD,
gestão de frota) em **[logistics-control/MERCADO.md](logistics-control/MERCADO.md)**
e implementei a **v2** com o que você pediu:
- **Motorista** (nome + **telefone**) vinculado ao veículo.
- **Combustível**: km/L × preço → **custo por rota** e **por mês**.
- **Manifesto/romaneio**: mercadorias por parada + **conferente** (quem recebeu) +
  **baixa** (status pendente/entregue/recusado), editável na tela.
- **Relatórios**: km **dia/semana/mês** por motorista, combustível no mês, gráficos.
- "**Que horas sair**" já vinha da janela de horário + ETA por parada.

**Próximos (escopo definido, faço na sequência autônoma):**
- **Magic (`mtg-deck-lab`)** — topo da fila. Vou fazer em **CustomTkinter**
  (desktop, abre com `.bat`/exe), **Commander + brackets (1–5)** + curva de mana +
  **preço em R$ (LigaMagic via scraping com cache)** + Scryfall para os dados.
- **Copa ao vivo (`worldcup-predictor` V2)** — integrar **API de futebol**
  (football-data.org / API-Football): resultados recentes, **chaveamento/grupos**,
  **próximos jogos** e dados de jogadores alimentando o modelo. Precisa de uma
  **chave gratuita**; vou deixar pronto para você colar a chave.

> Fim da sessão 2.

---

## 10. Sessão 3 — virada para "app produto / case fictício"

**Seu pedido:** em vez de "importe um CSV e veja", você quer **apps prontos, como
um case feito para uma empresa fictícia**, com KPIs e várias funcionalidades —
**bem completos**. Concordo totalmente — fica muito mais impressionante no
portfólio.

**O que fiz:** criei o **`festpro-suite`** — o painel de gestão completo da
empresa **fictícia** *FestPro Eventos & Locação*:
- **Dados embutidos e coerentes** (≈950 eventos em 13 meses, 150 clientes com
  recorrência, estoque, logística, financeiro) — gerados de forma determinística.
- **6 telas** (Visão Geral, Vendas, Eventos, Estoque, Logística, Financeiro) com
  **dezenas de KPIs** e gráficos (funil, ocupação de estoque com barra de
  progresso, aging de recebíveis, margem, NPS, no prazo, etc.).
- Tema próprio (violeta/âmbar) e **`EXECUTAR.bat`** de 1 clique.
- Verificado: **8 testes**, lint limpo, Streamlit HTTP 200 (porta **:8505**).

**Decisão de estilo (vale para os próximos):** os novos apps seguem este modelo
— **dados fictícios embutidos + muitos KPIs + várias telas**, "abre e usa". Os
apps antigos que pedem upload (finance, invest) continuam úteis como
**ferramentas**, mas posso reescrevê-los nesse estilo "case" se você quiser
(ex.: um banco fictício para o finance, uma gestora fictícia para o invest).

**Próximos (mantidos):** Magic em CustomTkinter (Commander/brackets/LigaMagic) e
Copa ao vivo (API de futebol). Ambos também no espírito "produto pronto".

> Fim da sessão 3.

---

## 11. Sessão 4 — Flask (adotado), Magic pronto e gestão real

**Flask:** você foi definitivo — adotei. A partir daqui, os apps "de gestão/web"
são em **Flask**. (Os apps de dados/BI já feitos em Streamlit continuam; posso
migrar pontualmente se quiser.)

**Li o seu `controle_coletas.py`** (Controle de Coletas v1.1) — é o padrão de
"gestão de verdade" que você quer no logística: importar, **editar**, dar **baixa**,
status/SLA com **feriados e dias úteis**, responsáveis, auditoria (quem/quando),
gravação atômica com backup e **file lock** para uso em rede. É exatamente o
espírito do próximo passo do logística (refeito em Flask, substituindo o Excel).

**Magic (mtg-deck-lab) — FEITO em Flask e testado ao vivo:**
- Cola **lista txt** ou **link** → parser → **Scryfall** (lote + cache) → análise.
- **Commander**: comandante, identidade de cor, **curva de mana**, tipos,
  tutores/turnos extra, **bracket (1–5)** com Game Changers + justificativa.
- **Preço** USD (Scryfall) + **R$ estimado**; **salva/lista decks**.
- **📷 Câmera** (getUserMedia) que **abre no celular** (Flask em `0.0.0.0`,
  mostra o IP da rede). Reconhecimento por **OCR (Tesseract, opcional)** + busca
  por nome como fallback garantido.
- Verificado: 12 testes, lint limpo, e **POST /analyze** com um deck do Atraxa
  retornou bracket + comandante + Game Changer (Rhystic Study) corretos.
- Rodando em **http://localhost:5000**.

**Por que não fiz a câmera com reconhecimento 100% automático agora:** OCR de
carta precisa do **Tesseract** (binário, como o FFmpeg) e a precisão na fonte das
cartas é mediana. Deixei o hook pronto + fallback por nome (que sempre funciona).
Evolução: matching por imagem (perceptual hash) contra a base do Scryfall.

**Próximos:** (1) **logística v3 em Flask** = app de gestão real (CRUD + baixa +
SLA/feriados + auditoria), no molde do `controle_coletas`; (2) **Copa ao vivo**
(API de futebol: resultados, chaveamento, próximos jogos, jogadores).

> Fim da sessão 4.

---

## Sessão 5 — Consertar o Git e "fazer vários, atualizando no Git"

**O que você pediu:** reverter o que eu tinha subido errado (misturei o portfólio
no seu repo de estudos), criar uma **pasta/repo dedicados**, e seguir construindo
**vários apps**, atualizando o Git a cada um.

| Decisão | Por quê |
|---|---|
| **Repo de estudos restaurado ao original** | Eu havia misturado os apps no `Projetos-Grupo-Desenvolvimento`. Fiz `reset --hard` + push forçado para devolver o repo ao estado certo (recursos_python/sql intactos). |
| **Pasta + repo novos: `portfolio-dev`** (privado) | Você escolheu o nome. Tudo do portfólio vive aqui agora: https://github.com/DiOliveira011/portfolio-dev |
| **Um commit por app** | Você pediu "ir atualizando no Git". Cada app entra com seu próprio commit, depois de passar em lint + testes + boot. |
| **Venvs em caminho curto** | OneDrive estoura o limite de 260 caracteres do Windows ao instalar libs aninhadas (Streamlit/sklearn). Cada `EXECUTAR.bat` cria o ambiente em `%LOCALAPPDATA%\portfolio-venvs\<app>`. |

**Apps construídos nesta sessão (todos verificados: ruff + pytest + boot HTTP 200):**

| App | Stack | O que entrega |
|---|---|---|
| `gestao-entregas` | Flask | Gestão **real** de entregas (no molde do seu `controle_coletas`): CRUD, **baixa com conferente**, **SLA em dias úteis com feriados BR**, status automático (Atrasado), KPIs e **auditoria**. Porta 5001. |
| `rpg-character-forge` | Flask | Fichas de **D&D 5e**: forjar/aleatório (4d6), cálculos completos, salvar e **ficha imprimível (PDF)**. Porta 5002. |
| `nfe-invoice-extractor` | Flask | Lê **NF-e (XML)**, extrai emitente/itens/totais, **valida** e exporta CSV. Porta 5003. |
| `ml-model-api-template` | FastAPI | Base **MLOps**: treina, serve `/predict` + `/health`, **Swagger /docs** e **Docker**. Porta 8000. |
| `churn-predictor` | Flask + sklearn | **Case** de evasão: base fictícia + RandomForest + **painel de risco** + simulador. Porta 5004. |
| `text-to-sql-analyst` | Flask | Pergunte ao banco **em português** → gera **SQL**, executa com guarda **SELECT-only**. Porta 5005. |
| `sales-bi-autoinsights` | Flask | BI que **escreve os próprios achados** a partir de dados embutidos. Porta 5006. |

**Decisão importante — "modo IA opcional":** em `text-to-sql-analyst` adotei o
padrão de **funcionar offline** (motor de regras) e **usar o Claude
automaticamente** se existir `ANTHROPIC_API_KEY`. Assim o app é útil e
**testável sem depender de chave**. Vou reusar esse padrão nos próximos de IA.

**Preferência sua reforçada (e seguida):** "app pronto/case", **não** "importe um
CSV e veja". Por isso `churn-predictor` e `sales-bi-autoinsights` já vêm com dados
realistas carregados e funcionalidades completas.

**Por que parei aqui (checkpoint):** os 4 que faltam têm uma **dependência real**:
- `rag-knowledge-assistant`, `ai-dungeon-master`, `doc-intelligence` → o valor está
  num **LLM** (Claude). Dá para entregar com o padrão "offline + Claude opcional",
  mas a parte de IA só brilha com `ANTHROPIC_API_KEY`.
- `mtg-card-vision` → reconhecer carta por foto **offline** é difícil (precisa de
  hashing perceptual contra base de imagens). O `mtg-deck-lab` já tem câmera +
  fallback por nome, então este é o de menor prioridade.

**Próximo passo proposto:** `rag-knowledge-assistant` com **recuperação offline
(TF-IDF)** + **geração via Claude quando houver chave** — verificável sem chave.

> Fim da sessão 5 (13 apps no ar).

---

## Sessão 6 — Os 3 apps de IA (Groq grátis + Claude + offline)

**O que você pediu:** construir os 3 de IA com "**offline + Claude opcional**" e
**também Groq, por ser gratuito**, como outra opção.

| Decisão | Por quê |
|---|---|
| **Camada LLM única: Groq + Claude + offline** | Cada app de IA tem um `llm.py` que detecta `GROQ_API_KEY` (grátis) ou `ANTHROPIC_API_KEY`. Sem chave → modo offline. Com as duas, `LLM_PROVIDER` decide. |
| **Chamadas via `urllib` (stdlib), sem SDK** | Não instala `anthropic`/`groq`/`openai`. Menos dependência, mais portável, e **offline-safe**: qualquer erro de rede vira `None` e cai no modo offline. |
| **Claude tem precedência quando ambas as chaves existem** | Qualidade; mas o Groq fica fácil de forçar (`LLM_PROVIDER=groq`) por ser grátis. |
| **Modelos padrão** | `llama-3.3-70b-versatile` (Groq) e `claude-sonnet-4-6` (Anthropic), ambos sobrescrevíveis por env. |

**Apps construídos (verificados: ruff + pytest + boot; IA testada sem rede via fallback):**

| App | Núcleo verificável offline | Com IA (Groq/Claude) |
|---|---|---|
| `rag-knowledge-assistant` (5007) | **Recuperação TF-IDF** (pure-Python) sobre a base de uma empresa fictícia; devolve os trechos. | Responde citando as fontes, usando só o contexto recuperado. |
| `ai-dungeon-master` (5008) | **Mestre offline**: classifica a ação + **rolagem d20** + flavor do cenário. | Narrativa viva com **memória de campanha** (histórico vira contexto). |
| `doc-intelligence` (5009) | Lê TXT/CSV/PDF/Excel, estatísticas, palavras-chave e **resumo extrativo**. | Resumo com título + pontos-chave gerado pela IA. |

**Resultado:** **16 de 17 apps** prontos e no Git. Só falta o `mtg-card-vision`
(reconhecer carta por foto), que depende de visão computacional mais pesada
(hashing perceptual contra base de imagens) — fica como o último, opcional.

**Como ligar a IA (qualquer um dos 3):** definir `GROQ_API_KEY` (grátis em
console.groq.com) **ou** `ANTHROPIC_API_KEY` antes de abrir o app. Nada muda no
código — o badge no topo passa de "Offline" para o provedor ativo.

> Fim da sessão 6 (16 apps no ar; IA com Groq/Claude/offline).

**Decisão de fechamento:** a seu pedido, o `mtg-card-vision` (reconhecer carta
por foto) fica como **ideia futura** — não foi construído. Motivo prático: visão
confiável exige modelo multimodal (com chave) ou hashing perceptual contra base
de imagens, e o `mtg-deck-lab` já entrega câmera no celular + busca por nome.
Portfólio encerrado com **16 apps** prontos, testados e no Git.

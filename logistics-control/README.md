# 🚚 Logistics Control — Distribuição B2B  ✅ *(v2 implementado)*

> Controle de **distribuição B2B** (rotas que vão **até empresas**, não delivery
> de comida): planeja e **otimiza rotas** (sweep + vizinho-mais-próximo + 2-opt)
> com **janela de horário** ("que horas sair pra chegar"), mostra no **mapa**, e
> ainda cuida do **motorista** (nome/telefone), **combustível** (R$/L → custo por
> rota), **manifesto/romaneio** (mercadorias + **conferente** + baixa) e
> **relatórios** de km e combustível por dia/semana/mês.

> 🏁 **Como executar:** dê **duplo clique em `EXECUTAR.bat`** (cria o ambiente e
> abre sozinho no navegador). Ou: `pip install -r requirements-dev.txt` +
> `streamlit run app.py`. Testes: `pytest` (11 testes).

> 📚 Pesquisa do que existe no mercado (TMS, canhoto digital, gestão de frota):
> veja **[MERCADO.md](./MERCADO.md)**.

## 🧭 Telas
- **Planejamento do dia:** KPIs (entregas, no prazo, km, **R$ de combustível**),
  mapa das rotas, romaneio por veículo (com motorista, litros e custo) e um
  **manifesto editável** para registrar **conferente** e dar **baixa** (status).
- **Motoristas & Frota:** km **dia/semana/mês** por motorista, **combustível no
  mês**, telefone, e gráficos de km e custo de combustível.

**Categoria:** Empresarial / Logística · **Skills:** Desenvolvimento · Dados · Otimização
**Stack sugerida:** Python · Streamlit · pandas · SQLite · heurística de roteirização · Plotly/pydeck (mapa)

## 🎯 Objetivo
Inspirado na operação da **RF Festas** (locação para eventos com frota própria de
entregas) e no universo **TGMOB / Lalamove / TMS de last-mile**: dar à operação
uma ferramenta para **planejar o dia** — quais entregas, em quais veículos, em que
ordem, chegando dentro das janelas combinadas — e **acompanhar a execução**.

## 🔎 O que o mercado faz (pesquisa) e o nosso diferencial
TMS/last-mile (Onfleet, Locus, Lalamove) oferecem: otimização de rota por janela
e capacidade, **auto-dispatch**, rastreio em tempo real + ETA, **prova de entrega**
(foto/assinatura/horário/GPS) e re-roteamento. Nosso MVP entrega o **núcleo
disso** de forma simples, offline e adaptada a uma operação de eventos
(entrega + **retirada/devolução** dos itens locados, que os genéricos ignoram).

## ✨ Funcionalidades (MVP)
- **Cadastros:** veículos (capacidade), motoristas, entregas (endereço, janela de
  horário, volume, tipo: entrega/retirada).
- **Planejamento:** atribuir entregas a veículos respeitando capacidade e janela;
  **ordenar a rota** com heurística (vizinho-mais-próximo + 2-opt).
- **Mapa** com os pontos e a sequência da rota; **status** (pendente/em rota/
  entregue/atrasado).
- **Prova de entrega**: marcar concluído com horário/observação.
- **Painel/KPIs**: entregas no prazo, ocupação da frota, km estimado, atrasos.

## 🧱 Arquitetura
- `core` (modelos: Veículo, Motorista, Entrega, Rota), `storage` (SQLite),
  `routing` (heurísticas de sequenciamento + checagem de janela/capacidade),
  `geo` (geocoding simples/coords + distâncias), `app` (Streamlit + mapa).

## 🗺️ Roadmap
- [ ] MVP: cadastros + planejamento/otimização + mapa + status + KPIs.
- [ ] V2: re-roteamento ao vivo, múltiplos veículos simultâneos, devoluções.
- [ ] V3: app do motorista (status pelo celular) e notificação de ETA ao cliente.

## 🎨 Tema
Paleta "logística" (azul + laranja/âmbar) — alta legibilidade, diferente dos demais.

## 📝 Origem
Pedido do briefing (esposa trabalha na RF Festas; antes Transgala→TGMOB).
Pesquei o que existe (Lalamove, TMS last-mile) para fazer algo enxuto e melhor
para o caso de **eventos/locação**.

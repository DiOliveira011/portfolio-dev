# 🚚 Gestão de Entregas (Flask)  ✅

> App de **gestão operacional** de entregas — para **gerenciar de verdade**, não só
> ver KPI. A ideia: trocar a planilha de Excel por um app onde a equipe **cadastra**
> entregas, acompanha o **status/SLA** e **dá baixa** registrando o **conferente**
> (quem recebeu). Inspirado num controle real de operações.

**Skills:** Desenvolvimento web (Flask) · regras de negócio (SLA/feriados) · CRUD
**Stack:** Python 3.12 · Flask · armazenamento JSON (atômico) · zero dependências pesadas

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** (ou `pip install -r requirements-dev.txt` +
`python app.py`). Abre em **http://localhost:5001** — e **no celular** pelo IP que
aparece no terminal (mesma Wi-Fi). Já vem com uma operação de exemplo carregada.

## ✨ O que faz
- **Cadastro / edição** de entregas (cliente, local/praça, responsável, data,
  valor, observações).
- **SLA / prazo automático**: calcula o prazo em **dias úteis**, pulando fins de
  semana e **feriados nacionais** (inclui Carnaval, Sexta-feira Santa, Corpus
  Christi). Diz "que dia tem que estar entregue".
- **Status**: Pendente → Em rota → Entregue; **Atrasado** é detectado sozinho
  quando passa do prazo sem baixa.
- **Dar baixa**: marca como entregue registrando **conferente** e data/hora.
- **Filtros** (status, responsável, busca) e **KPIs** (pendentes, em rota,
  entregues, **atrasadas**, **% no prazo**, valor em aberto).
- **Auditoria**: criado/editado por quem e quando.

## 🧱 Arquitetura
```
gestao-entregas/
├── app.py                 # rotas Flask (lista, nova, editar, baixa, excluir)
├── src/gentregas/
│   ├── holidays.py        # feriados BR + dias úteis (SLA)
│   ├── core.py            # domínio: status, prazo, baixa, enrich
│   ├── store.py           # persistência JSON (escrita atômica)
│   └── sample.py          # operação de exemplo (seed)
├── templates/  static/    # UI responsiva (tema teal corporativo)
└── tests/                 # feriados, domínio e storage (18 testes)
```

## 🧪 Testes
`pytest` — feriados/dias úteis, regras de status/SLA e CRUD do storage.

## 🗺️ Próximos
- Importar planilha (CSV/Excel) e exportar relatórios.
- Histórico de alterações por entrega e backup automático.
- Login por usuário (hoje usa o usuário do Windows na auditoria).

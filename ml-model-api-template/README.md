# 🤖 ML Model API Template (FastAPI + scikit-learn + Docker)  ✅

> **Base de MLOps** pronta para reusar: treina um modelo, **serializa o artefato**
> e o serve por uma **API FastAPI** com `/predict`, `/health`, `/model/info` e
> **documentação interativa (Swagger) em `/docs`**. Vem com **Dockerfile** e
> **testes**. Troque o dataset em `mlapi/train.py` e o resto continua funcionando.

**Skills:** Engenharia de IA / MLOps · APIs (FastAPI) · empacotamento (Docker) · testes
**Stack:** Python 3.12 · FastAPI · scikit-learn · joblib · uvicorn · pytest

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** (cria o ambiente, treina e sobe a API) ou:
```bash
pip install -r requirements-dev.txt
python -m mlapi.train        # treina e salva o artefato em artifacts/
python app.py                # sobe a API em http://localhost:8000
```
Abra **http://localhost:8000/docs** para testar pelo navegador (Swagger).

### Docker
```bash
docker build -t ml-api .
docker run -p 8000:8000 ml-api
```

## 🔌 Endpoints
| Método | Rota | O que faz |
|--------|------|-----------|
| GET | `/health` | status + versão do modelo |
| GET | `/model/info` | features, classes e **métricas** do treino |
| POST | `/predict` | recebe as features e devolve **classe + probabilidades** |
| GET | `/docs` | Swagger interativo |

Exemplo:
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
# -> {"label":"setosa","prediction_index":0,"probabilities":{...}}
```

## 🧱 Arquitetura
```
ml-model-api-template/
├── app.py                 # entrypoint (uvicorn)
├── Dockerfile             # treina na build e serve com uvicorn
├── src/mlapi/
│   ├── train.py           # ← troque o dataset/modelo aqui
│   ├── model.py           # carrega o artefato (treina se faltar) e prediz
│   ├── schema.py          # contrato da API (Pydantic) + validação
│   └── api.py             # rotas FastAPI
└── tests/                 # treino e API (6 testes, TestClient)
```

## 🧪 Testes
`pytest` — treino atinge acurácia esperada e a API responde/valida (inclui 422
para payload inválido). *Exemplo atual: Iris, acurácia ~0.92.*

## 🗺️ Próximos
- Versionamento de modelo + registro de experimentos (MLflow).
- CI (GitHub Actions) rodando testes e build da imagem.

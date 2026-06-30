# 🧠 Doc Intelligence  *(projeto final — #15)*

> Você joga um **PDF ou Excel** e recebe: um **resumo do conteúdo**, os
> **principais resultados/insights**, e **informações técnicas** sobre o arquivo
> e sobre os dados. Tudo com uma **IA acoplada**.

**Categoria:** Engenharia de IA + Ciência de Dados · **Skills:** IA (LLM) · Data
**Stack sugerida:** Python · API da Claude · pandas · openpyxl · pdfplumber/PyMuPDF · Streamlit

## 🎯 Objetivo
Uma ferramenta de **inteligência documental** que lê arquivos heterogêneos e
gera um relatório automático, combinando **análise determinística** (estatística
dos dados) com **interpretação por IA** (resumo e conclusões em linguagem
natural). É a síntese de quase tudo do portfólio.

## 💼 Valor para o portfólio
Projeto "vitrine": une parsing de documentos, análise de dados e LLM num produto
que qualquer empresa entende o valor (ganho de tempo na leitura de relatórios,
planilhas e documentos). Fecha a trilha Dev → Data → IA.

## ✨ Funcionalidades (MVP)
- **Excel/CSV:** perfil dos dados (linhas, colunas, tipos, nulos, estatísticas),
  detecção de tabelas, KPIs e gráficos automáticos.
- **PDF:** extração de texto/tabelas e metadados do arquivo.
- **Resumo por IA:** a Claude recebe a análise estruturada + amostras e produz:
  resumo executivo, principais resultados, achados/anomalias e próximos passos.
- **Ficha técnica:** infos do arquivo (tamanho, páginas/abas, encoding) e dos
  dados (schema, qualidade, intervalos).
- Exportar o relatório (Markdown/PDF).

## 🧱 Arquitetura
- `readers/` (excel, csv, pdf → representação comum), `analysis/` (perfil +
  estatística + gráficos), `ai/` (monta o contexto e chama a Claude com
  *tool/JSON output*), `report/` (montagem + export), `app/` (Streamlit).
- Reaproveita o motor de **RAG** (#12) para documentos longos e o
  **profiling** do **sales-bi-autoinsights** (#10).

## 🗺️ Roadmap
- [ ] MVP: Excel/CSV → análise + resumo por IA + ficha técnica.
- [ ] V2: PDF (texto/tabelas) e perguntas livres sobre o arquivo (chat).
- [ ] V3: lote de arquivos, comparação entre versões e templates de relatório.

## 🤖 IA — como entra
A IA **não** "lê o arquivo cru": nós extraímos e resumimos os dados de forma
estruturada e enviamos esse contexto (schema, estatísticas, amostras, trechos)
para a Claude gerar a interpretação. Isso mantém a resposta **fundamentada nos
dados reais** e controla custo/contexto.

## 📚 Notas
- Modelo padrão: Claude (Anthropic). Requer `ANTHROPIC_API_KEY`.
- Processa arquivos locais; ideal rodar offline para o parsing e só a etapa de
  resumo usar a API.

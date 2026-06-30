# 🧾 NF-e Invoice Extractor

> Extrai, valida e estrutura dados de **notas fiscais eletrônicas** (NF-e) a
> partir de **PDF/XML** e exporta para planilha/banco.

**Categoria:** Finanças/Dados (empresarial) · **Skills:** Desenvolvimento · IA (OCR)
**Stack sugerida:** Python · lxml (XML NF-e) · pdfplumber · (opcional) Tesseract OCR · pandas

## 🎯 Objetivo
Automatizar a leitura de notas fiscais: do XML padrão SEFAZ (campos estruturados)
e de PDFs (DANFE) via parsing/OCR, normalizando emitente, destinatário, itens,
impostos e totais.

## 💼 Valor para o portfólio
Caso **empresarial real** (financeiro/contábil/fiscal). Mostra parsing robusto,
validação de dados e automação que economiza horas de digitação.

## ✨ Funcionalidades (MVP)
- Ler XML de NF-e e extrair campos-chave (CNPJ, itens, valores, impostos).
- Ler PDF de DANFE (texto; OCR como fallback) e mapear os mesmos campos.
- Validar (chave de acesso, somatórios) e exportar para Excel/CSV/SQLite.

## 🧱 Arquitetura
- `parsers/xml`, `parsers/pdf`, `core` (modelo da nota), `validate`,
  `export`. Mesmo modelo de saída para XML e PDF.

## 🗺️ Roadmap
- [ ] MVP: XML → modelo → Excel, com validações.
- [ ] V2: PDF/DANFE com OCR de fallback.
- [ ] V3: processamento em lote + painel de conferência.

## 📚 Notas
- Base: layout oficial da NF-e (SEFAZ). Processa arquivos locais.

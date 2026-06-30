# 📸 MTG Card Vision

> Reconhece uma carta de **Magic** a partir de uma **foto** e devolve nome,
> edição e preço — visão computacional aplicada.

**Categoria:** Mundo Nerd · **Skills:** Engenharia de IA (Visão Computacional)
**Stack sugerida:** Python · OpenCV · Pillow · pHash / ORB · (opcional) PyTorch · Scryfall API

## 🎯 Objetivo
Identificar cartas por imagem usando duas abordagens: (1) **perceptual hashing /
feature matching** contra a base de imagens da Scryfall (rápido, sem treino) e,
como evolução, (2) um **classificador CNN** para casos difíceis.

## 💼 Valor para o portfólio
Projeto de IA "palpável": pipeline de visão computacional ponta a ponta —
captura, pré-processamento, matching/inferência e avaliação de acurácia.

## ✨ Funcionalidades (MVP)
- Carregar imagem/usar webcam; detectar e recortar a carta (contornos/perspectiva).
- Casar com a carta correta via pHash/ORB sobre a base Scryfall.
- Mostrar nome, edição, preço e link; medir acurácia em um conjunto de teste.

## 🧱 Arquitetura
- `vision/preprocess` (detecção+retificação), `vision/match` (hashing/feature),
  `data/scryfall` (download de imagens + índice), `app` (CLI/GUI), `eval`.

## 🗺️ Roadmap
- [ ] MVP: matching por pHash/ORB com webcam/imagem.
- [ ] V2: dataset rotulado + CNN (transfer learning) e métricas de acurácia.
- [ ] V3: leitura em lote (escanear uma coleção) e exportar planilha de inventário.

## 📚 Dados / APIs
- Scryfall (imagens de alta resolução + metadados).

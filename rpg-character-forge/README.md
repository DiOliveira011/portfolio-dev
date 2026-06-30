# ⚔️ RPG Character Forge

> Criador de fichas de personagem para **D&D 5e**, **Old Dragon** e
> **Daggerheart**, com regras aplicadas e exportação em PDF.

**Categoria:** Mundo Nerd · **Skills:** Desenvolvimento (arquitetura/regras)
**Stack sugerida:** Python · CustomTkinter · pydantic · ReportLab (PDF) · JSON de regras

## 🎯 Objetivo
Guiar a criação de personagens respeitando as regras de cada sistema (atributos,
classes, raças/ancestralidades, perícias) e gerar uma **ficha em PDF** pronta
para a mesa.

## 💼 Valor para o portfólio
Excelente para mostrar **modelagem de domínio** e um motor de regras extensível:
adicionar um novo sistema = adicionar um módulo de regras, sem mexer no resto.

## ✨ Funcionalidades (MVP)
- Seleção de sistema e passo a passo de criação com validação das regras.
- Cálculo automático de modificadores, CA, PV, perícias.
- Exportar ficha em PDF e salvar/abrir em JSON.

## 🧱 Arquitetura
- `rules/<sistema>` (definições e validações por sistema), `core` (modelos
  comuns de ficha), `export/pdf`, `gui`. Strategy pattern para sistemas.

## 🗺️ Roadmap
- [ ] MVP: D&D 5e completo + export PDF.
- [ ] V2: Old Dragon e Daggerheart; templates de ficha customizáveis.
- [ ] V3: rolagem de dados integrada e "nível up" assistido.

## 📚 Referências
- SRDs/licenças abertas de cada sistema (usar conteúdo livre/SRD quando houver).

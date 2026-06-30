# 🐉 AI Dungeon Master

> Um **Mestre de RPG com IA** que conduz aventuras de mesa (D&D / Daggerheart),
> narra cenas, controla NPCs e **lembra** o que aconteceu na campanha.

**Categoria:** Mundo Nerd · **Skills:** Engenharia de IA (LLM, memória/RAG)
**Stack sugerida:** Python · API da Claude (Anthropic) · SQLite/embeddings · CustomTkinter ou Discord bot

## 🎯 Objetivo
Criar um mestre virtual que recebe as ações dos jogadores e responde com
narração coerente, aplica rolagens de dados e mantém **estado de campanha**
(personagens, lugares, missões) usando memória de longo prazo.

## 💼 Valor para o portfólio
Mostra domínio de **LLMs aplicados**: engenharia de prompt, *tool use* (rolar
dados, consultar regras), memória persistente e controle de contexto.

## ✨ Funcionalidades (MVP)
- Conversa com o mestre por texto; narração + perguntas aos jogadores.
- *Tool use*: rolar dados (d20 etc.) e aplicar resultados na narrativa.
- Memória de campanha: resumos automáticos por sessão (evita estourar contexto).

## 🧱 Arquitetura
- `llm` (cliente Claude + prompts + tools), `memory` (resumos + recuperação),
  `game` (estado/personagens/dados), `ui` (chat). RAG sobre o histórico.

## 🗺️ Roadmap
- [ ] MVP: chat + rolagem de dados + memória por resumo.
- [ ] V2: fichas dos jogadores e regras de combate por turnos.
- [ ] V3: geração de mapas/imagens de cena e exportação do "diário de campanha".

## 📚 Notas de IA
- Modelo padrão: Claude (Anthropic). Requer `ANTHROPIC_API_KEY`.

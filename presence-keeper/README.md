# 🟢 Presence Keeper

Utilitário pessoal que **mantém a estação de trabalho ativa** durante
apresentações, leituras longas, chamadas e processos demorados — evitando que a
**tela entre em suspensão** e que o **status de presença** fique como *ausente*.

> Utilitário de **desktop (Windows)** — demonstra integração com a **Win32 API**
> (via `ctypes`) e interface em **Tkinter**. Usa apenas biblioteca padrão.

## ▶️ Como usar
**Opção 1 — executável:** **duplo clique em `PresenceKeeper.exe`** (não precisa ter
Python instalado).

**Opção 2 — com Python:** **duplo clique em `INICIAR.bat`** (ou
`python presence_keeper.py`).

Na janela:
1. Marque o que deseja manter (tela ligada / sessão ativa).
2. Opcional: escolha um **desligamento automático** (1h, 2h, 4h, 8h).
3. Clique em **Ativar**. Para encerrar, clique em **Desativar** ou feche a janela.

O painel mostra **há quanto tempo o sistema está ocioso** e o **horário do último
sinal** — assim dá para ver que está funcionando.

## ⚙️ Como funciona (mecanismos oficiais do Windows)
- **Tela não suspende:** `SetThreadExecutionState` com
  `ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED` — a mesma API que players de vídeo e
  softwares de apresentação usam para impedir a suspensão.
- **Sessão permanece ativa:** a cada ~60s envia a tecla virtual **F15**. Essa
  tecla **não existe em teclados físicos** e é **ignorada por aplicativos**;
  serve apenas para zerar o contador de inatividade do sistema (que é o que faz o
  status virar *ausente*). Não move o mouse nem digita nada visível.

Requisito: **Windows + Python 3** (usa só biblioteca padrão — `tkinter` e
`ctypes`, sem instalar nada).

## ✅ Verificação
`python presence_keeper.py --selftest` executa um teste do núcleo (ativa, envia o
sinal, confirma que a ociosidade cai e restaura o estado de energia) sem abrir a
janela.

## ⚠️ Observações
- Em máquinas corporativas, **políticas de grupo (GPO)** podem forçar bloqueio de
  tela por tempo — nesses casos o sistema operacional tem a palavra final.
- Encerrar o app **restaura** o comportamento normal de energia imediatamente.

"""Presence Keeper — mantém a sessão de trabalho ativa.

Evita que a tela entre em suspensão e que o status de presença fique "ausente"
durante apresentações, leituras longas, chamadas e processos demorados.

Como funciona (mecanismos oficiais/limpos do Windows):
  • Tela ligada: SetThreadExecutionState (ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED)
    — a mesma API que players de vídeo e apresentações usam para não suspender.
  • Sessão ativa: a cada N segundos envia a tecla virtual F15, que não existe em
    teclados físicos e é ignorada por aplicativos — serve apenas para zerar o
    contador de inatividade do sistema (usado para marcar "ausente").

Uso:
  python presence_keeper.py            -> abre a janela
  python presence_keeper.py --selftest -> testa o núcleo sem abrir a janela
"""

from __future__ import annotations

import ctypes
import sys
import threading
import time

# --- Win32 constants -----------------------------------------------------------
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

VK_F15 = 0x7E
KEYEVENTF_KEYUP = 0x0002
INPUT_KEYBOARD = 1

_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32

_kernel32.SetThreadExecutionState.restype = ctypes.c_uint
_kernel32.SetThreadExecutionState.argtypes = [ctypes.c_uint]


# --- SendInput plumbing (F15 no-op keystroke) ----------------------------------
_PUL = ctypes.POINTER(ctypes.c_ulong)


class _KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                ("dwExtraInfo", _PUL)]


class _MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong), ("dwExtraInfo", _PUL)]


class _HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class _InputUnion(ctypes.Union):
    _fields_ = [("ki", _KeyBdInput), ("mi", _MouseInput), ("hi", _HardwareInput)]


class _Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", _InputUnion)]


_user32.SendInput.argtypes = (ctypes.c_uint, ctypes.POINTER(_Input), ctypes.c_int)
_user32.SendInput.restype = ctypes.c_uint


class _LastInputInfo(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]


def _send_f15() -> None:
    """Send a harmless F15 key tap (down+up) to reset the idle timer."""
    extra = ctypes.c_ulong(0)
    down = _Input(INPUT_KEYBOARD,
                  _InputUnion(ki=_KeyBdInput(VK_F15, 0, 0, 0, ctypes.pointer(extra))))
    up = _Input(INPUT_KEYBOARD,
                _InputUnion(ki=_KeyBdInput(VK_F15, 0, KEYEVENTF_KEYUP, 0,
                                           ctypes.pointer(extra))))
    _user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(_Input))
    _user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(_Input))


def _set_exec_state(keep_display: bool) -> None:
    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    if keep_display:
        flags |= ES_DISPLAY_REQUIRED
    _kernel32.SetThreadExecutionState(flags)


def _clear_exec_state() -> None:
    _kernel32.SetThreadExecutionState(ES_CONTINUOUS)


def idle_seconds() -> float:
    """Seconds since the last real user input (what 'ausente' is based on)."""
    info = _LastInputInfo()
    info.cbSize = ctypes.sizeof(info)
    _user32.GetLastInputInfo(ctypes.byref(info))
    return max(0.0, (_kernel32.GetTickCount() - info.dwTime) / 1000.0)


class Keeper:
    """Background worker that keeps the machine awake and the session active."""

    def __init__(self, interval: int = 59) -> None:
        self.interval = interval
        self.keep_display = True
        self.keep_presence = True
        self.active = False
        self.last_ping: float | None = None
        self.stop_at: float | None = None        # epoch time, or None = sem limite
        self._thread: threading.Thread | None = None

    def start(self, duration_seconds: int | None = None) -> None:
        if self.active:
            return
        self.active = True
        self.stop_at = (time.time() + duration_seconds) if duration_seconds else None
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.active = False
        if self._thread and self._thread.is_alive() and threading.current_thread() is not self._thread:
            self._thread.join(timeout=2)
        _clear_exec_state()

    def _run(self) -> None:
        while self.active:
            _set_exec_state(self.keep_display)
            if self.keep_presence:
                _send_f15()
                self.last_ping = time.time()
            # dorme em passos de 1s para parar rápido e respeitar o auto-desligar
            for _ in range(max(1, self.interval)):
                if not self.active:
                    break
                if self.stop_at and time.time() >= self.stop_at:
                    self.active = False
                    break
                time.sleep(1)
        _clear_exec_state()


def _selftest() -> int:
    print("Presence Keeper — autoteste do núcleo")
    print(f"  Ocioso agora: {idle_seconds():.1f}s")
    k = Keeper(interval=2)
    k.start()
    print("  Ativado (tela+presença). Enviando F15 e mantendo desperto...")
    time.sleep(3)
    print(f"  Último sinal F15: {'ok' if k.last_ping else 'nenhum'}")
    print(f"  Ocioso após ping: {idle_seconds():.1f}s (deve estar baixo)")
    k.stop()
    print("  Desativado e estado de energia restaurado. OK.")
    return 0


def run_gui() -> None:
    import tkinter as tk
    from datetime import datetime

    BG, CARD, INK, MUTED = "#0f172a", "#1e293b", "#e2e8f0", "#94a3b8"
    GREEN, RED, ACCENT = "#22c55e", "#ef4444", "#14b8a6"

    keeper = Keeper()

    root = tk.Tk()
    root.title("Presence Keeper")
    root.configure(bg=BG)
    root.geometry("440x500")
    root.resizable(False, False)

    tk.Label(root, text="Presence Keeper", bg=BG, fg=INK,
             font=("Segoe UI Semibold", 20)).pack(pady=(22, 2))
    tk.Label(root, text="Mantém a tela ligada e a sessão ativa",
             bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack()

    pill = tk.Label(root, text="○  Inativo", bg=BG, fg=MUTED,
                    font=("Segoe UI Semibold", 15))
    pill.pack(pady=(18, 8))

    toggle = tk.Button(root, text="Ativar", bd=0, relief="flat",
                       bg=GREEN, fg="#06281a", activebackground=GREEN,
                       font=("Segoe UI Semibold", 14), width=18, height=1,
                       cursor="hand2")
    toggle.pack(pady=4)

    opts = tk.Frame(root, bg=CARD)
    opts.pack(fill="x", padx=22, pady=16, ipady=6)

    var_display = tk.BooleanVar(value=True)
    var_presence = tk.BooleanVar(value=True)

    def _mk_check(parent, text, var):
        return tk.Checkbutton(parent, text=text, variable=var, bg=CARD, fg=INK,
                              selectcolor=CARD, activebackground=CARD, activeforeground=INK,
                              font=("Segoe UI", 10), anchor="w", padx=10, pady=4,
                              highlightthickness=0, bd=0)

    _mk_check(opts, "Manter a tela ligada (não suspender)", var_display).pack(fill="x")
    _mk_check(opts, "Manter a sessão ativa (evitar “ausente”)", var_presence).pack(fill="x")

    dur_frame = tk.Frame(root, bg=BG)
    dur_frame.pack(fill="x", padx=22)
    tk.Label(dur_frame, text="Desligar automaticamente após:", bg=BG, fg=MUTED,
             font=("Segoe UI", 10)).pack(side="left")
    dur_var = tk.StringVar(value="Nunca")
    _DUR = {"Nunca": None, "1 hora": 3600, "2 horas": 7200, "4 horas": 14400, "8 horas": 28800}
    dur_menu = tk.OptionMenu(dur_frame, dur_var, *_DUR.keys())
    dur_menu.configure(bg=CARD, fg=INK, activebackground=ACCENT, bd=0, highlightthickness=0,
                       font=("Segoe UI", 10))
    dur_menu["menu"].configure(bg=CARD, fg=INK)
    dur_menu.pack(side="right")

    info = tk.Label(root, text="", bg=BG, fg=MUTED, font=("Consolas", 10), justify="left")
    info.pack(pady=14)

    footer = tk.Label(root, text="Usa APIs oficiais do Windows. Feche a janela para encerrar.",
                      bg=BG, fg="#64748b", font=("Segoe UI", 8))
    footer.pack(side="bottom", pady=8)

    def apply_opts() -> None:
        keeper.keep_display = var_display.get()
        keeper.keep_presence = var_presence.get()

    def toggle_action() -> None:
        if keeper.active:
            keeper.stop()
        else:
            apply_opts()
            keeper.start(_DUR.get(dur_var.get()))

    def refresh() -> None:
        if keeper.active:
            pill.configure(text="●  Ativo", fg=GREEN)
            toggle.configure(text="Desativar", bg=RED, fg="#2a0a0a", activebackground=RED)
            ping = (datetime.fromtimestamp(keeper.last_ping).strftime("%H:%M:%S")
                    if keeper.last_ping else "—")
            restante = ""
            if keeper.stop_at:
                secs = max(0, int(keeper.stop_at - time.time()))
                restante = f"\nDesliga em:    {secs // 3600:02d}:{secs % 3600 // 60:02d}:{secs % 60:02d}"
            info.configure(text=(f"Ocioso há:     {idle_seconds():4.0f} s\n"
                                 f"Último sinal:  {ping}{restante}"))
        else:
            pill.configure(text="○  Inativo", fg=MUTED)
            toggle.configure(text="Ativar", bg=GREEN, fg="#06281a", activebackground=GREEN)
            info.configure(text=f"Ocioso há:     {idle_seconds():4.0f} s\n(desativado)")
        root.after(1000, refresh)

    def on_close() -> None:
        keeper.stop()
        root.destroy()

    toggle.configure(command=toggle_action)
    var_display.trace_add("write", lambda *_: apply_opts())
    var_presence.trace_add("write", lambda *_: apply_opts())
    root.protocol("WM_DELETE_WINDOW", on_close)
    refresh()
    root.mainloop()


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    run_gui()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

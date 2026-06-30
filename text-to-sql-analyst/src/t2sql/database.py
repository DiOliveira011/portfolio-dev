"""Build and seed an in-memory SQLite sales database (deterministic)."""

from __future__ import annotations

import random
import sqlite3
from datetime import date, timedelta

SCHEMA = """
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL
);
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    regiao TEXT NOT NULL
);
CREATE TABLE vendas (
    id INTEGER PRIMARY KEY,
    data TEXT NOT NULL,            -- YYYY-MM-DD
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    quantidade INTEGER NOT NULL,
    valor REAL NOT NULL
);
"""

_PRODUTOS = [
    ("Notebook Pro 14", "Eletrônicos", 5200.0),
    ("Smartphone X", "Eletrônicos", 3100.0),
    ("Fone Bluetooth", "Eletrônicos", 290.0),
    ("Monitor 27\"", "Eletrônicos", 1450.0),
    ("Cafeteira Inox", "Casa", 350.0),
    ("Jogo de Panelas", "Casa", 480.0),
    ("Aspirador Robô", "Casa", 1600.0),
    ("Tênis de Corrida", "Esporte", 420.0),
    ("Bicicleta Urbana", "Esporte", 2300.0),
    ("Mochila Trilha", "Esporte", 260.0),
    ("Livro: Clean Code", "Livros", 130.0),
    ("Livro: SQL na Prática", "Livros", 95.0),
]
_REGIOES = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
_FIRST = ["Ana", "Bruno", "Carla", "Diego", "Elaine", "Felipe", "Gabriela", "Hugo",
          "Isa", "João", "Karina", "Lucas", "Marina", "Nelson", "Olívia", "Paulo"]
_LAST = ["Silva", "Souza", "Costa", "Pereira", "Lima", "Gomes", "Ribeiro", "Rocha"]


def build_connection(
    seed: int = 7, n_clientes: int = 120, n_vendas: int = 2600
) -> sqlite3.Connection:
    """Return an in-memory SQLite connection seeded with synthetic sales data."""
    rng = random.Random(seed)
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.executescript(SCHEMA)

    conn.executemany(
        "INSERT INTO produtos (id, nome, categoria, preco) VALUES (?,?,?,?)",
        [(i + 1, nome, cat, preco) for i, (nome, cat, preco) in enumerate(_PRODUTOS)],
    )
    clientes = [
        (i + 1, f"{rng.choice(_FIRST)} {rng.choice(_LAST)}", rng.choice(_REGIOES))
        for i in range(n_clientes)
    ]
    conn.executemany("INSERT INTO clientes (id, nome, regiao) VALUES (?,?,?)", clientes)

    start = date(2025, 7, 1)
    vendas = []
    for i in range(n_vendas):
        prod_id = rng.randint(1, len(_PRODUTOS))
        preco = _PRODUTOS[prod_id - 1][2]
        qtd = rng.randint(1, 5)
        dia = start + timedelta(days=rng.randint(0, 364))
        vendas.append((i + 1, dia.isoformat(), prod_id, rng.randint(1, n_clientes),
                       qtd, round(preco * qtd, 2)))
    conn.executemany(
        "INSERT INTO vendas (id, data, produto_id, cliente_id, quantidade, valor) "
        "VALUES (?,?,?,?,?,?)", vendas,
    )
    conn.commit()
    return conn


def schema_text() -> str:
    """Human/LLM-readable description of the schema."""
    return (
        "Tabelas (SQLite):\n"
        "• produtos(id, nome, categoria, preco)\n"
        "• clientes(id, nome, regiao)\n"
        "• vendas(id, data 'YYYY-MM-DD', produto_id→produtos.id, "
        "cliente_id→clientes.id, quantidade, valor)"
    )

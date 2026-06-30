"""Service: holds the seeded DB and answers questions safely."""

from __future__ import annotations

import sqlite3

from t2sql.database import build_connection, schema_text
from t2sql.nl2sql import generate_sql, is_safe_select


class AnalystService:
    def __init__(self, seed: int = 7) -> None:
        self.conn = build_connection(seed)
        self.schema = schema_text()

    def stats(self) -> dict:
        def count(table: str) -> int:
            return self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        return {"produtos": count("produtos"), "clientes": count("clientes"),
                "vendas": count("vendas")}

    def ask(self, question: str) -> dict:
        question = (question or "").strip()
        if not question:
            return {"ok": False, "error": "Digite uma pergunta."}
        sql, source = generate_sql(question, self.schema)
        if not sql:
            return {"ok": False,
                    "error": "Não entendi a pergunta. Tente uma das sugestões abaixo."}
        if not is_safe_select(sql):
            return {"ok": False, "sql": sql,
                    "error": "Por segurança, só executo consultas SELECT (somente leitura)."}
        try:
            cur = self.conn.execute(sql)
            columns = [d[0] for d in cur.description]
            rows = [list(r) for r in cur.fetchall()[:200]]
            return {"ok": True, "sql": sql, "source": source,
                    "columns": columns, "rows": rows}
        except sqlite3.Error as exc:
            return {"ok": False, "sql": sql, "error": f"Erro ao executar a query: {exc}"}

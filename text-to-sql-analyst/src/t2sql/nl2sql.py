"""Natural language → SQL: safety guard, deterministic rules, optional Claude."""

from __future__ import annotations

import os
import re
import unicodedata

_FORBIDDEN = ("insert", "update", "delete", "drop", "alter", "create",
              "attach", "detach", "pragma", "replace", "truncate", "vacuum")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text).strip()


def is_safe_select(sql: str) -> bool:
    """Allow a single read-only SELECT/WITH statement only."""
    s = sql.strip().rstrip(";").strip()
    if not s:
        return False
    low = s.lower()
    if not (low.startswith("select") or low.startswith("with")):
        return False
    if ";" in s:                      # mais de uma instrução
        return False
    return not any(re.search(rf"\b{w}\b", low) for w in _FORBIDDEN)


# --- Deterministic rules (offline mode) ---------------------------------------

_TOP_PRODUTOS = (
    "SELECT p.nome, ROUND(SUM(v.valor),2) AS faturamento, SUM(v.quantidade) AS unidades "
    "FROM vendas v JOIN produtos p ON p.id = v.produto_id "
    "GROUP BY p.id ORDER BY faturamento DESC LIMIT 10"
)
_POR_MES = (
    "SELECT substr(data,1,7) AS mes, ROUND(SUM(valor),2) AS faturamento "
    "FROM vendas GROUP BY mes ORDER BY mes"
)
_POR_REGIAO = (
    "SELECT c.regiao, ROUND(SUM(v.valor),2) AS faturamento "
    "FROM vendas v JOIN clientes c ON c.id = v.cliente_id "
    "GROUP BY c.regiao ORDER BY faturamento DESC"
)
_POR_CATEGORIA = (
    "SELECT p.categoria, ROUND(SUM(v.valor),2) AS faturamento "
    "FROM vendas v JOIN produtos p ON p.id = v.produto_id "
    "GROUP BY p.categoria ORDER BY faturamento DESC"
)
_MELHORES_CLIENTES = (
    "SELECT c.nome, c.regiao, ROUND(SUM(v.valor),2) AS total "
    "FROM vendas v JOIN clientes c ON c.id = v.cliente_id "
    "GROUP BY c.id ORDER BY total DESC LIMIT 10"
)


def rule_based(question: str) -> str | None:
    """Map a Portuguese question to SQL using keyword heuristics."""
    q = normalize(question)

    def has(*words: str) -> bool:
        return any(w in q for w in words)

    if has("mes", "mensal", "por mes", "evolucao") and has("venda", "fatur", "receita"):
        return _POR_MES
    if has("regiao", "regioes", "estado"):
        return _POR_REGIAO
    if has("categoria", "categorias"):
        return _POR_CATEGORIA
    if has("produto", "produtos") and has("mais vendid", "top", "melhor", "ranking", "campeao"):
        return _TOP_PRODUTOS
    if has("cliente", "clientes") and has("melhor", "top", "mais compra", "maior", "fiel"):
        return _MELHORES_CLIENTES
    if has("ticket medio", "ticket", "valor medio", "media por venda"):
        return "SELECT ROUND(AVG(valor),2) AS ticket_medio FROM vendas"
    if has("quantos", "numero", "quantidade", "total de", "quantas") and has("cliente"):
        return "SELECT COUNT(*) AS clientes FROM clientes"
    if has("quantas", "quantos", "numero", "quantidade", "total de") and has("venda", "pedido"):
        return "SELECT COUNT(*) AS vendas FROM vendas"
    if has("fatur", "receita", "faturou") or (has("total") and has("venda")):
        return "SELECT ROUND(SUM(valor),2) AS faturamento_total FROM vendas"
    if has("produto", "catalogo", "preco", "lista"):
        return "SELECT id, nome, categoria, preco FROM produtos ORDER BY categoria, nome"
    return None


# --- Optional Claude mode -----------------------------------------------------

def llm_available() -> bool:
    if not os.getenv("ANTHROPIC_API_KEY"):
        return False
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return True


def _llm_generate(question: str, schema: str) -> str | None:
    try:
        import anthropic
        client = anthropic.Anthropic()
        system = (
            "Você converte perguntas em uma única query SQL para SQLite. "
            "Responda APENAS com a query SELECT, sem explicação e sem markdown.\n\n" + schema
        )
        msg = client.messages.create(
            model="claude-opus-4-8", max_tokens=400, system=system,
            messages=[{"role": "user", "content": question}],
        )
        text = "".join(b.text for b in msg.content if getattr(b, "type", None) == "text")
        text = re.sub(r"```sql|```", "", text).strip()
        return text or None
    except Exception:  # noqa: BLE001 - qualquer falha cai para as regras
        return None


def generate_sql(question: str, schema: str) -> tuple[str | None, str | None]:
    """Return (sql, source). source ∈ {'IA (Claude)', 'Regras'} ou (None, None)."""
    if llm_available():
        sql = _llm_generate(question, schema)
        if sql and is_safe_select(sql):
            return sql, "IA (Claude)"
    sql = rule_based(question)
    if sql:
        return sql, "Regras"
    return None, None

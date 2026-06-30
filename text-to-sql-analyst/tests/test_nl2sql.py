"""Tests for safety guard and rule-based NL→SQL."""

from __future__ import annotations

from t2sql.nl2sql import generate_sql, is_safe_select, rule_based


def test_safe_select_allows_reads() -> None:
    assert is_safe_select("SELECT * FROM vendas")
    assert is_safe_select("  with x as (select 1) select * from x ;")


def test_safe_select_blocks_writes_and_injection() -> None:
    assert not is_safe_select("DROP TABLE vendas")
    assert not is_safe_select("DELETE FROM vendas")
    assert not is_safe_select("SELECT 1; DROP TABLE vendas")
    assert not is_safe_select("UPDATE vendas SET valor=0")
    assert not is_safe_select("")


def test_rules_map_known_questions() -> None:
    assert "GROUP BY mes" in rule_based("faturamento por mês")
    assert "regiao" in rule_based("vendas por região")
    assert "categoria" in rule_based("vendas por categoria")
    assert "LIMIT 10" in rule_based("top produtos mais vendidos")
    assert "AVG(valor)" in rule_based("qual o ticket médio?")
    assert "COUNT(*)" in rule_based("quantos clientes temos?")


def test_rules_unknown_returns_none() -> None:
    assert rule_based("qual a previsão do tempo amanhã?") is None


def test_generate_sql_offline_uses_rules() -> None:
    sql, source = generate_sql("faturamento total", "schema")
    assert source == "Regras"
    assert is_safe_select(sql)

"""Aggregations + the auto-insight narrative engine."""

from __future__ import annotations

from collections import defaultdict

from salesbi import fmt_brl


def total_revenue(data: list[dict]) -> float:
    return round(sum(r["valor"] for r in data), 2)


def by_dimension(data: list[dict], key: str) -> dict[str, float]:
    acc: dict[str, float] = defaultdict(float)
    for r in data:
        acc[r[key]] += r["valor"]
    return {k: round(v, 2) for k, v in sorted(acc.items(), key=lambda kv: kv[1], reverse=True)}


def monthly_series(data: list[dict]) -> list[tuple[str, float]]:
    acc: dict[str, float] = defaultdict(float)
    for r in data:
        acc[r["mes"]] += r["valor"]
    return [(m, round(acc[m], 2)) for m in sorted(acc)]


def _growth(series: list[tuple[str, float]]) -> float:
    first, last = series[0][1], series[-1][1]
    return (last - first) / first if first else 0.0


def kpis(data: list[dict]) -> dict:
    series = monthly_series(data)
    cats = by_dimension(data, "categoria")
    regs = by_dimension(data, "regiao")
    total = total_revenue(data)
    best = max(series, key=lambda t: t[1])
    worst = min(series, key=lambda t: t[1])
    return {
        "total": total,
        "meses": len(series),
        "media_mensal": round(total / len(series), 2) if series else 0.0,
        "crescimento": _growth(series),
        "melhor_mes": best,
        "pior_mes": worst,
        "categoria_lider": next(iter(cats)),
        "regiao_lider": next(iter(regs)),
    }


def generate_insights(data: list[dict]) -> list[str]:
    """Produce a human-readable list of findings — the 'auto' in auto-insights."""
    series = monthly_series(data)
    cats = by_dimension(data, "categoria")
    regs = by_dimension(data, "regiao")
    total = sum(cats.values())
    bullets: list[str] = []

    growth = _growth(series)
    verbo = "cresceu" if growth >= 0 else "recuou"
    bullets.append(
        f"O faturamento {verbo} {abs(growth) * 100:.1f}% no período "
        f"(de {fmt_brl(series[0][1])} para {fmt_brl(series[-1][1])})."
    )

    best = max(series, key=lambda t: t[1])
    worst = min(series, key=lambda t: t[1])
    bullets.append(
        f"Melhor mês: {best[0]} ({fmt_brl(best[1])}); "
        f"pior mês: {worst[0]} ({fmt_brl(worst[1])})."
    )

    lider = next(iter(cats))
    bullets.append(
        f"Categoria líder: {lider}, com {cats[lider] / total * 100:.0f}% do faturamento."
    )

    cat_growth = {}
    for cat in cats:
        cs = monthly_series([r for r in data if r["categoria"] == cat])
        cat_growth[cat] = _growth(cs)
    up = max(cat_growth, key=lambda c: cat_growth[c])
    down = min(cat_growth, key=lambda c: cat_growth[c])
    bullets.append(
        f"Em ascensão: {up} ({cat_growth[up] * 100:+.0f}%); "
        f"em retração: {down} ({cat_growth[down] * 100:+.0f}%)."
    )

    rl = next(iter(regs))
    share_rl = regs[rl] / sum(regs.values()) * 100
    bullets.append(f"Região destaque: {rl}, respondendo por {share_rl:.0f}% das vendas.")

    canais_first = by_dimension([r for r in data if r["mes"] == series[0][0]], "canal")
    canais_last = by_dimension([r for r in data if r["mes"] == series[-1][0]], "canal")
    share_first = canais_first.get("E-commerce", 0) / sum(canais_first.values()) * 100
    share_last = canais_last.get("E-commerce", 0) / sum(canais_last.values()) * 100
    if share_last - share_first > 1:
        bullets.append(
            f"Canal em expansão: e-commerce passou de {share_first:.0f}% para "
            f"{share_last:.0f}% do mix — vale reforçar o digital."
        )

    media = sum(v for _, v in series) / len(series)
    picos = [m for m, v in series if v > media * 1.25]
    if picos:
        bullets.append(
            f"Picos de demanda (>25% acima da média) em: {', '.join(picos)} — "
            "atenção a estoque e logística nesses meses."
        )
    return bullets

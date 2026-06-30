"""Category taxonomy and keyword rules (Brazilian Portuguese).

Categories are plain strings so they round-trip cleanly to CSV/SQLite and to the
ML classifier's labels. ``KEYWORD_RULES`` maps a category to substrings commonly
found in transaction descriptions/merchants.
"""

from __future__ import annotations

from typing import Final

#: Category used for income (positive amounts).
INCOME_CATEGORY: Final[str] = "Renda"

#: Category used when nothing else matches.
UNCATEGORIZED: Final[str] = "Outros"

#: Canonical expense categories shown in the UI.
CATEGORIES: Final[list[str]] = [
    "Mercado",
    "Alimentação",
    "Transporte",
    "Moradia",
    "Saúde",
    "Educação",
    "Lazer",
    "Assinaturas",
    "Compras",
    "Viagem",
    "Impostos e Taxas",
    "Investimentos",
    "Transferências",
    INCOME_CATEGORY,
    UNCATEGORIZED,
]

#: Lowercase keyword → category. Matching is substring, case/accent-insensitive
#: (see :func:`findash.categorize.rules.normalize`).
KEYWORD_RULES: Final[dict[str, list[str]]] = {
    "Mercado": [
        "supermercado", "mercado", "carrefour", "pao de acucar", "assai",
        "atacadao", "big", "extra", "hortifruti", "sacolao", "zaffari", "mambo",
    ],
    "Alimentação": [
        "ifood", "rappi", "restaurante", "lanchonete", "padaria", "bar ",
        "burger", "pizza", "mc donalds", "mcdonalds", "starbucks", "cafe",
        "uber eats", "doceria", "food",
    ],
    "Transporte": [
        "uber", "99 ", "99app", "99pop", "cabify", "posto", "ipiranga", "shell",
        "petrobras", "br distribuidora", "metro", "metrô", "cptm", "passagem",
        "estacionamento", "pedagio", "pedágio", "combustivel", "gasolina",
    ],
    "Moradia": [
        "aluguel", "condominio", "condomínio", "energia", "enel", "light",
        "cpfl", "sabesp", "agua", "água", "gas ", "comgas", "iptu", "internet",
        "vivo fibra", "claro", "net ", "telefonica",
    ],
    "Saúde": [
        "farmacia", "farmácia", "drogaria", "drogasil", "pacheco", "raia",
        "hospital", "clinica", "clínica", "laboratorio", "laboratório",
        "unimed", "amil", "plano de saude", "dentista", "psicolog",
    ],
    "Educação": [
        "escola", "faculdade", "universidade", "curso", "udemy", "alura",
        "coursera", "livraria", "mensalidade", "matricula", "matrícula",
    ],
    "Lazer": [
        "cinema", "cinemark", "netflix", "spotify", "youtube premium", "steam",
        "playstation", "xbox", "nintendo", "ingresso", "show", "teatro",
        "parque", "game", "twitch",
    ],
    "Assinaturas": [
        "netflix", "spotify", "amazon prime", "disney", "hbo", "max ", "globoplay",
        "icloud", "google one", "microsoft 365", "office 365", "assinatura",
        "deezer", "paramount",
    ],
    "Compras": [
        "amazon", "mercado livre", "mercadolivre", "magalu", "magazine luiza",
        "americanas", "shopee", "aliexpress", "shein", "renner", "riachuelo",
        "zara", "centauro", "casas bahia", "kabum", "pichau",
    ],
    "Viagem": [
        "latam", "gol ", "azul ", "decolar", "booking", "airbnb", "hotel",
        "hostel", "cvc", "passagem aerea", "passagem aérea", "123milhas",
    ],
    "Impostos e Taxas": [
        "tarifa", "taxa", "juros", "iof", "anuidade", "imposto", "darf",
        "multa", "ir ", "tributo",
    ],
    "Investimentos": [
        "aplicacao", "aplicação", "investimento", "tesouro", "cdb", "corretora",
        "xp investimentos", "rico", "nuinvest", "btg", "clear", "renda fixa",
        "acoes", "ações",
    ],
    "Transferências": [
        "pix", "ted", "doc ", "transferencia", "transferência", "transf ",
        "saque", "deposito", "depósito",
    ],
    INCOME_CATEGORY: [
        "salario", "salário", "pagamento", "provento", "rendimento",
        "restituicao", "restituição", "reembolso", "pro labore", "pró-labore",
    ],
}

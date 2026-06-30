"""Adventure scenarios — flavor used by the offline DM and as LLM context."""

from __future__ import annotations

SCENARIOS: dict[str, dict] = {
    "A Masmorra do Dragão Adormecido": {
        "intro": ("Tochas tremeluzem nas paredes úmidas de pedra. Ao longe, uma "
                  "respiração colossal ecoa pelos corredores. Você está na entrada "
                  "da masmorra onde dorme o dragão Vermithrax sobre seu tesouro."),
        "areas": ["um corredor de pedra coberto de runas", "uma ponte sobre um abismo escuro",
                  "uma câmara com estátuas de cavaleiros petrificados",
                  "um salão dourado onde o dragão repousa"],
        "npcs": ["um goblin tagarela acorrentado", "o espírito de um cavaleiro caído",
                 "uma mercadora misteriosa de capuz"],
        "clues": ["marcas de garras enormes no chão", "uma inscrição: 'só o silêncio passa'",
                  "um baú entreaberto brilhando ao longe"],
        "enemies": ["dois goblins batedores", "um golem de pedra", "morcegos de caverna"],
        "itens": ["uma espada élfica", "uma poção de cura", "uma chave de osso"],
    },
    "A Taverna Amaldiçoada": {
        "intro": ("A chuva bate nas janelas da taverna 'O Javali Cego'. Os clientes "
                  "estão imóveis, congelados no tempo desde a meia-noite. Só você se "
                  "move — e algo observa das sombras da adega."),
        "areas": ["o salão principal com clientes congelados", "a cozinha fria e silenciosa",
                  "a adega escura cheia de barris", "os quartos do andar de cima"],
        "npcs": ["o taverneiro sussurrando avisos", "uma criança fantasma rindo",
                 "um andarilho encapuzado bebendo sozinho"],
        "clues": ["um relógio parado à meia-noite", "pegadas molhadas que sobem a escada",
                  "um diário com a última página rasgada"],
        "enemies": ["sombras que rastejam", "um cliente possuído", "um espectro vingativo"],
        "itens": ["um amuleto de prata", "uma vela que nunca apaga", "uma adaga enferrujada"],
    },
    "A Floresta dos Sussurros": {
        "intro": ("A névoa engole as árvores retorcidas. Vozes sussurram seu nome "
                  "entre as folhas. Você procura o santuário perdido no coração da "
                  "Floresta dos Sussurros, onde dizem morar uma bruxa antiga."),
        "areas": ["uma trilha coberta de cogumelos luminosos", "um riacho de água negra",
                  "um círculo de pedras antigas", "a cabana torta da bruxa"],
        "npcs": ["um cervo de olhos humanos", "um lenhador perdido há anos",
                 "a própria bruxa, gentil e terrível"],
        "clues": ["fitas vermelhas amarradas nos galhos", "ossos pequenos formando uma seta",
                  "uma canção que vem de lugar nenhum"],
        "enemies": ["lobos espectrais", "uma raiz animada", "um espantalho que anda"],
        "itens": ["um galho-varinha", "um frasco de luz", "um mapa rabiscado"],
    },
}


def scenario_names() -> list[str]:
    return list(SCENARIOS)

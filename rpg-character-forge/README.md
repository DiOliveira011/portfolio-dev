# ⚔️ RPG Character Forge (Flask)  ✅

> Forja fichas de personagem de **D&D 5e** prontas: escolha raça, classe e
> atributos (ou **role um aleatório**) e o app calcula **modificadores, PV, CA,
> iniciativa, testes de resistência e perícias**. Salva os personagens e tem
> **ficha imprimível** (vira PDF pelo navegador). Abre no **celular** também.

**Skills:** Desenvolvimento web (Flask) · modelagem de regras · UI imprimível
**Stack:** Python 3.12 · Flask · só biblioteca padrão (sem dependências pesadas)

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** (ou `pip install -r requirements-dev.txt` +
`python app.py`). Abre em **http://localhost:5002** — e no celular pelo IP que
aparece no terminal (mesma Wi-Fi).

## ✨ O que faz
- **Forjar** por escolha (raça, classe, nível, 6 atributos) → ficha completa.
- **🎲 Aleatório**: rola **4d6 (descarta o menor)** e monta tudo, colocando o
  maior valor no atributo principal da classe.
- **Cálculos 5e**: modificadores, **bônus de proficiência** por nível, **PV**
  (dado de vida + CON), **CA**, iniciativa, **testes de resistência** e
  **perícias** (com proficiência da classe), percepção passiva.
- **Salvar / Meus personagens** e **imprimir** (PDF).
- **8 raças** e **8 classes** (conteúdo livre/SRD).

## 🧱 Arquitetura
```
rpg-character-forge/
├── app.py                 # rotas Flask
├── src/rpgforge/
│   ├── data.py            # raças, classes, perícias
│   ├── sheet.py           # modificadores, proficiência, montagem da ficha
│   ├── generator.py       # rolagem 4d6 + personagem aleatório
│   └── store.py           # salvar/listar (JSON)
├── templates/  static/    # UI (tema fantasia), ficha imprimível
└── tests/                 # regras de ficha e gerador (10 testes)
```

## 🗺️ Próximos
- **Old Dragon** e **Daggerheart** (trocar o módulo de regras pelo sistema).
- Seleção de perícias na tela e equipamento inicial.

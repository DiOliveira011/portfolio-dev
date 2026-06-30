# 📚 Logística B2B / Distribuição — o que existe no mercado

> Pesquisa para embasar o **logistics-control**. Importante: **não é** entrega
> tipo iFood/pizzaria (last-mile de consumo). Aqui é **distribuição B2B**: rotas
> que vão **até empresas**, levam as mercadorias dela, com **conferente**,
> **romaneio/manifesto**, **canhoto** e **gestão de motorista/frota**.

## 🧩 As 3 famílias de software que cobrem esse caso

### 1) TMS — Transportation Management System (gestão de transporte)
O "ERP do transporte". No Brasil: **ESL TMS Web Cloud**, **Bsoft TMS**,
**Transportadora Pro**, **Fretefy**, **Senior**, **TRB**.
Funções típicas:
- **Roteirização inteligente** (ordem e trajeto das entregas) e sequenciamento.
- **Romaneio / manifesto de carga** (o que vai em cada rota).
- **Baixa de entregas** (status: entregue, recusado, parcial).
- Emissão de **CT-e** e **MDF-e**, cubagem de veículo, custo de frete.
- Integração com **ERP** e acompanhamento em tempo real.

### 2) Canhoto digital / comprovante de entrega (POD)
Substitui o canhoto de papel. No Brasil: **Comprovei**, **Easy Doc**,
**ComprovaFácil**, **Dynamicca**.
Funções típicas:
- Registro de **quem recebeu** (o "conferente"), assinatura e **foto/canhoto**.
- **Validade jurídica**, data/hora e geolocalização da entrega.
- Sincronização em **tempo real** com o sistema central.

### 3) Gestão de frota (telemetria, combustível, motorista)
Geotab, Samsara, AssetWorks, Fleetrabbit, e nacionais (KMM).
Funções típicas:
- **Consumo de combustível** por veículo / motorista / rota / período.
- **Quilometragem** (dia/semana/mês), horas dirigidas, ociosidade.
- Relatórios **agendados** (diário/semanal/mensal) e exportação.
- **Comportamento do motorista** (excesso de velocidade, frenagem) — economia
  reportada de 5–15% de combustível.
- Integração com **cartão de combustível**.

## 🎯 O que o nosso projeto faz (recorte e diferencial)
Pegamos o **núcleo** das 3 famílias num app simples, local e voltado a uma
operação de **distribuição/eventos** (como a RF Festas):

| Necessidade sua | Onde entra no app |
|---|---|
| Rotas que vão até a **empresa** | Planejamento de rota (sweep + 2-opt) |
| **Que horas sair** para chegar na hora | Janela de horário + ETA por parada |
| **Conferente** (quem recebeu) | Campo no manifesto / baixa da entrega |
| **Quais mercadorias** foram | Itens (romaneio) por parada |
| **Motorista + telefone** | Cadastro de motorista vinculado ao veículo |
| **Km rodado** (dia/semana/mês) | Relatório por motorista/veículo |
| **Combustível gasto** | Consumo (km/l) × preço → custo por rota e período |

**O que deixamos de fora de propósito (por ora):** emissão fiscal (CT-e/MDF-e),
telemetria por GPS em tempo real e cartão de combustível — são camadas de
integração pesadas; ficam como evolução (V2/V3).

## 🔗 Fontes
- TMS BR: ESL Sistemas, Bsoft, Transportadora Pro, Fretefy, TRB.
- Canhoto digital: Comprovei, Easy Doc, ComprovaFácil, Dynamicca, TOTVS (conceito).
- Gestão de frota/combustível: Geotab, AssetWorks, Fleetrabbit.

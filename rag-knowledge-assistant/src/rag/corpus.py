"""Knowledge base of a fictional company (Nimbus Tecnologia) — the RAG corpus."""

from __future__ import annotations

COMPANY = "Nimbus Tecnologia"

#: title -> document text. In a real app these viriam de PDFs/Notion/Confluence.
DOCS: dict[str, str] = {
    "Política de Férias": (
        "Todo colaborador CLT tem direito a 30 dias de férias por período "
        "aquisitivo de 12 meses. As férias podem ser divididas em até três "
        "períodos, sendo um deles de no mínimo 14 dias corridos. O agendamento "
        "deve ser feito no portal RH com pelo menos 30 dias de antecedência e "
        "aprovado pelo gestor. É permitido vender até 10 dias de férias (abono "
        "pecuniário). Férias não gozadas em dobro são pagas conforme a CLT."
    ),
    "Trabalho Remoto e Horários": (
        "A Nimbus adota modelo híbrido: 3 dias remotos e 2 presenciais por "
        "semana. O horário é flexível, com janela núcleo das 10h às 16h em que "
        "todos devem estar disponíveis. A jornada é de 8 horas diárias. Reuniões "
        "devem ser agendadas dentro do horário núcleo sempre que possível. "
        "Trabalho 100% remoto exige aprovação do diretor da área."
    ),
    "Benefícios": (
        "Os benefícios incluem vale-refeição de R$ 40 por dia útil, vale-"
        "alimentação de R$ 800 por mês, plano de saúde Bradesco sem coparticipação "
        "para o titular, plano odontológico, Gympass (academia) e seguro de vida. "
        "Há também o day off de aniversário: um dia de folga na semana do seu "
        "aniversário. Auxílio home office de R$ 120 por mês para internet."
    ),
    "Reembolso de Despesas": (
        "Despesas a trabalho (viagens, transporte por aplicativo, materiais) são "
        "reembolsáveis. Abra a solicitação no portal Financeiro anexando a nota "
        "fiscal em até 30 dias da despesa. Reembolsos aprovados pelo gestor são "
        "pagos junto com o salário do mês seguinte. O limite para refeições em "
        "viagem é de R$ 90 por dia sem aprovação prévia."
    ),
    "Segurança da Informação": (
        "Use senhas fortes e únicas, guardadas no gerenciador 1Password fornecido "
        "pela empresa. A autenticação em dois fatores (2FA) é obrigatória em todos "
        "os sistemas. Nunca compartilhe credenciais. Desconfie de e-mails de "
        "phishing pedindo senha ou pagamento urgente — reporte para "
        "seguranca@nimbus.com. Dados de clientes não podem ser copiados para "
        "dispositivos pessoais."
    ),
    "Onboarding de Novos Colaboradores": (
        "Nos primeiros dias você recebe o notebook configurado, os acessos aos "
        "sistemas e um mentor (buddy) para te acompanhar nas duas primeiras "
        "semanas. O RH agenda as integrações de cultura, segurança e benefícios. "
        "Até o fim do primeiro mês, você e seu gestor definem as metas do período "
        "de experiência (90 dias)."
    ),
    "Suporte de TI": (
        "Para problemas com equipamento, acessos ou software, abra um chamado no "
        "portal de TI (ti.nimbus.com) ou no canal #suporte-ti. O SLA de "
        "atendimento é de 1 dia útil para prioridade normal e 4 horas para "
        "urgências que impeçam o trabalho. Troca de equipamento padrão acontece a "
        "cada 3 anos. Periféricos podem ser solicitados pelo mesmo portal."
    ),
}

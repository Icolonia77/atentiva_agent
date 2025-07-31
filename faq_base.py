# faq_base.py

import re

FAQ_TEXT = """
Com certeza! Vamos conversar sobre o que as fontes nos dizem sobre a ATENTIVA, explorando os detalhes que a definem no contexto mais amplo do seu setor.
A ATENTIVA é uma empresa consolidada no setor de transportes, especializada no transporte de segurados. Ela tem uma história de mais de 12 anos de atuação e está no mercado desde 2013. A sede da empresa está estrategicamente localizada em Sumaré/SP, na região de Campinas.
Qual é o principal serviço da ATENTIVA? A ATENTIVA se posiciona como uma das principais empresas de transportes para segurados. O serviço consiste em transportar pessoas que possuem apólice de seguro veicular. Se o veículo do segurado tiver algum problema, como pane, batida ou sinistro, e ele solicitar um transporte à seguradora, a ATENTIVA é acionada para garantir esse deslocamento.
Estrutura e Abrangência Operacional: A empresa demonstra uma estrutura robusta para atender à sua demanda:
• Sua sede opera 24 horas por dia, 7 dias por semana, garantindo que os clientes possam contar com sua estrutura e eficiência a qualquer momento.
• A ATENTIVA conta com uma vasta rede de mais de 500 motoristas parceiros.
• Possui mais de 30 colaboradores diretos e mais de 50 indiretos (prestadores de serviços).
• Sua estrutura interna é bem organizada, com setores específicos para cada demanda, incluindo financeiro, fiscal, RH, operacional e logístico, qualidade, além de governança e presidência.
• A reputação da empresa é alta, com a avaliação máxima de 5 estrelas no Google.
Parcerias com Motoristas: Ganhos e Requisitos As fontes fornecem detalhes importantes para motoristas interessados em ser parceiros da ATENTIVA:
• Remuneração:
o O pagamento é feito por KM rodado, no valor de R$ 1,10 por KM.
o A ATENTIVA usa o critério de pagar a corrida integral (ida e volta), mesmo sem passageiro na volta.
o A contagem da corrida começa a partir da aceitação e envio da localização.
o Para corridas de até 40KM (ida e volta), o motorista recebe um valor fixo de R$ 44,00.
o Se a corrida ultrapassar 40KM, o pagamento volta a ser por KM rodado.
o Pedágios são reembolsados tanto na ida quanto na volta.
o Há um adicional de R$ 80,00 para corridas que ultrapassam 1000KM (ida e volta), sendo R$ 80,00 a cada 1000KM.
o Horas Paradas (HPs) são pagas (R$ 17 por HP), geralmente aplicadas quando o motorista chega ao ponto de embarque antes do guincho e informa a central.
• Requisitos para Cadastro:
o Ter EAR na CNH (ou ter até 12 dias para regularizar após iniciar o cadastro).
o Ter MEI ou CNPJ para emissão de NF (é possível iniciar como pessoa física, mas a regularização será necessária; pode-se emitir NF por terceiros).
o O veículo não pode ultrapassar 12 anos de uso, precisa ter 4 portas, ar-condicionado gelando, e estar limpo e bem cuidado. Se tiver rodas de ferro, precisa de calotas.
o O veículo precisa estar com CRLV em dia e pode ser próprio, emprestado ou alugado.
o É necessário ter conta bancária e chave PIX no mesmo banco para recebimento.
o Ter CNH digital e CRLV versão digital.
o Ter comprovante de endereço completo e CEP.
o Quatro fotos atuais do veículo (frente, traseira e duas laterais).
o Seguro Corporativo do App: É obrigatório (imposição das seguradoras) e cobre socorro médico e hospitalar em caso de acidente, com cobertura de até R$ até 100 mil para pessoas. O custo é de R$ 200 anual, mas o parceiro paga apenas R$ 100, sendo o restante pago pela ATENTIVA. O valor é debitado no primeiro faturamento do parceiro e tem validade de 12 meses. O motorista também é beneficiário.
o Certidão de Antecedentes Criminais (gerada via gov.br).
Boas Condutas e Operacional: A ATENTIVA enfatiza a importância de um serviço de qualidade e boa conduta:
• Ser gentil e cordial com os passageiros e evitar assuntos controversos (times, religiões, políticas, gênero).
• Usar roupas adequadas, evitando regatas, bermudas, bonés, chinelos.
• Não usar celular para atendimento ou digitação com o passageiro embarcado, apenas via Bluetooth para casos extremamente importantes.
• Atender rapidamente ligações ou mensagens da central.
• Chegar ao ponto de embarque o mais breve possível (prazo de 40 minutos após aceite da corrida).
• Jamais permitir que o segurado dirija o veículo do parceiro.
• Sugerir paradas seguras em viagens longas.
• Sempre avisar sobre atrasos no chat do app e WhatsApp.
• Jamais mudar a rota sugerida pelo Google Maps, pois o sistema é integrado.
• Não criticar seguradoras, pois a ATENTIVA presta serviços para todas.
• Não aceitar corridas se estiver cansado.
• Informar a central sobre a chegada do guincho para solicitar HPs.
• Não tentar realizar reparos no veículo do segurado.
• Se houver pets sem caixa de transporte, avisar o operacional.
• O segurado tem direito a apenas um destino. Mudanças de destino só com autorização da seguradora e ciência da ATENTIVA.
• Ligar para o segurado em caso de dificuldades de localização.
• Digitar a placa do veículo do segurado no app para validação da corrida após a chegada.
Cancelamentos e Engajamento do Parceiro:
• Cancelamento pelo segurado/seguradora: Se ocorrer em até 15 minutos, o parceiro recebe meia saída (R$ 22,00). Se ocorrer após 16 minutos, recebe a saída inteira (R$ 44,00).
• Cancelamento pelo parceiro: Não há remuneração, independente do tempo ou percurso.
• Importância de informar HPs: É crucial que o parceiro informe o operacional para que a solicitação seja feita à seguradora.
• Disponibilidade no App: Evitar ficar off por mais de 4 dias para não inativar o login e evitar recusas sequenciais. É recomendado ficar conectado apenas se houver disponibilidade real.
• Feedback do Segurado: Ao finalizar a corrida, pedir que o segurado avalie o serviço via link.
• Não Exclusividade: A ATENTIVA não exige exclusividade, permitindo que os parceiros trabalhem com outros aplicativos.
• Demanda e Ganhos: A demanda não é tão alta quanto em apps como Uber ou 99, mas as corridas são "muito rentáveis". A empresa afirma que os prestadores que ficam mais logados e disponíveis são os que mais trabalham e, consequentemente, mais ganham.
• Flexibilidade de Horário: O parceiro determina sua própria disponibilidade, reforçando que ele é um prestador de serviços.
• É possível solicitar a inativação do cadastro sem custo caso não haja adaptação.
Processo de Cadastro: Após a conversa inicial e o envio de respostas, o próximo passo é o envio de documentos para dar sequência ao cadastro. Os documentos essenciais são:
• Foto da CNH (preferencialmente digital em PDF).
• Foto do CRLV do veículo (preferencialmente digital em PDF).
• Dados bancários e chave PIX da mesma conta (informar CNPJ se for jurídica).
• Certificado MEI.
• Quatro fotos atuais dos quatro lados do veículo.
• Endereço completo e CEP.
• Atestado de Antecedentes Criminais.
Após o envio dos documentos, a ATENTIVA libera o acesso ao treinamento e ao aplicativo para início das atividades. Para dúvidas, o contato de Ricardo Ferreiro é 19 99686-8581.
Em resumo, a ATENTIVA se apresenta como uma oportunidade de parceria para motoristas, oferecendo uma estrutura de suporte completa, remuneração clara e flexibilidade, enquanto foca em um nicho de mercado específico (transportes para segurados) com alta qualidade de serviço e boa reputação.
"""

THEMES = {
    "remuneração": {
        "regex": r"Remuneração:(.*?)(?=(Requisitos para Cadastro|Boas Condutas|Processo de Cadastro|Cancelamentos|$))",
        "keywords": [
            "pagamento", "paga", "remuneração", "valor", "km", "corrida", "preço", "quanto paga", "salário", "reembolso", "pedágio", "fixo", "HP", "parada", "adicional", "ganho", "pro labore"
        ],
    },
    "cadastro": {
        "regex": r"Processo de Cadastro:(.*?)(?=(Remuneração|Requisitos para Cadastro|Boas Condutas|Cancelamentos|$))",
        "keywords": [
            "como cadastro", "cadastrar", "como entrar", "quero entrar", "documento", "documentos", "envio", "como funciona o cadastro"
        ],
    },
    "requisitos": {
        "regex": r"Requisitos para Cadastro:(.*?)(?=(Remuneração|Boas Condutas|Processo de Cadastro|Cancelamentos|$))",
        "keywords": [
            "requisito", "requisitos", "necessário", "precisa", "preciso", "pode", "exigência", "critérios", "condição", "documentação"
        ],
    },
    "seguro": {
        "regex": r"Seguro Corporativo do App:(.*?\.)",
        "keywords": [
            "seguro", "apólice", "cobertura", "segurado", "indenização", "sinistro", "acidente"
        ],
    },
    "conduta": {
        "regex": r"Boas Condutas e Operacional:(.*?)(?=(Remuneração|Requisitos para Cadastro|Processo de Cadastro|Cancelamentos|$))",
        "keywords": [
            "conduta", "comportamento", "postura", "pode", "não pode", "atitude", "uniforme", "roupa", "vestimenta", "gentileza", "educação"
        ],
    },
    "cancelamento": {
        "regex": r"Cancelamentos e Engajamento do Parceiro:(.*?)(?=(Remuneração|Requisitos para Cadastro|Processo de Cadastro|Boas Condutas|$))",
        "keywords": [
            "cancelamento", "cancela", "parada", "desistir", "engajamento", "parar", "recusar", "não aceitar"
        ],
    },
    "estrutura": {
        "regex": r"Estrutura e Abrangência Operacional:(.*?)(?=(Remuneração|Requisitos para Cadastro|Boas Condutas|Processo de Cadastro|Cancelamentos|$))",
        "keywords": [
            "estrutura", "empresa", "sede", "onde fica", "quantos motoristas", "quantos funcionários", "funcionários", "diretores", "time", "opera", "região", "abrangência", "cidade", "local"
        ],
    },
    "empresa": {
        "regex": r"A ATENTIVA é uma empresa consolidada.*?Sumaré/SP, na região de Campinas\.",
        "keywords": [
            "empresa", "sobre", "história", "fundação", "quando começou", "quem é", "atentiva"
        ],
    },
    "contato": {
        "regex": r"Para dúvidas, o contato de Ricardo Ferreiro é 19 99686-8581.",
        "keywords": [
            "contato", "whatsapp", "telefone", "falar com", "ajuda", "suporte", "assistência"
        ],
    },
}

def get_faq_answer(question):
    question = question.lower()

    for tema, bloco in THEMES.items():
        for k in bloco["keywords"]:
            if k in question:
                match = re.search(bloco["regex"], FAQ_TEXT, re.IGNORECASE | re.DOTALL)
                if match:
                    resposta = match.group(0).strip()
                    # Limpa caracteres indesejados
                    resposta = re.sub(r"\n\s*", "\n", resposta)
                    resposta = re.sub(r"•\s*", "- ", resposta)
                    return resposta
    # Busca por "documento" mesmo fora do cadastro
    if "documento" in question or "documentação" in question:
        return "Documentos para cadastro: Foto da CNH (preferencialmente digital em PDF), Foto do CRLV do veículo (preferencialmente digital em PDF), Dados bancários e chave PIX, Certificado MEI, Quatro fotos atuais dos quatro lados do veículo, Endereço completo e CEP, Atestado de Antecedentes Criminais."

    # Resposta padrão
    return (
        "Aqui está um resumo sobre a ATENTIVA:\n\n"
        "A ATENTIVA é uma empresa consolidada no setor de transportes, especializada no transporte de segurados desde 2013, com sede em Sumaré/SP. "
        "Tem avaliação máxima no Google e estrutura robusta (24h, mais de 500 motoristas parceiros). "
        "Oferece remuneração clara, suporte completo, cadastro ágil, requisitos técnicos/legais bem definidos e destaca conduta ética. "
        "Qualquer pergunta específica, envie novamente!"
    )


# faq_base.py

# FAQ_TEXT = """
# A ATENTIVA é uma empresa consolidada no setor de transportes, especializada no transporte de segurados. 
# História: 12+ anos, fundada em 2013, sede Sumaré/SP.
# Principal serviço: transporte de segurados a pedido das seguradoras.
# Estrutura: 24h, +500 motoristas parceiros, 30+ colaboradores diretos.
# Avaliação: 5 estrelas no Google.
# Remuneração: R$1,10/km, ida e volta. Corridas até 40km: R$44 fixo. Pedágios e HPs pagos.
# Requisitos: EAR na CNH, MEI/CNPJ, veículo <12 anos, 4 portas, ar-condicionado, CRLV digital, conta bancária/PIX, fotos do veículo, seguro do app obrigatório, antecedentes criminais.
# Condutas: cordialidade, seguir rota, não usar celular com passageiro, atender central rápido.
# Cadastro: enviar docs, realizar treinamento, receber acesso ao app.
# Dúvidas? Contato: Ricardo Ferreiro 19 99686-8581.
# """

# def get_faq_answer(question):
#     # Resposta simples baseada em keyword (pode expandir usando LLM)
#     keywords = {
#         "remuneração": "O pagamento é R$1,10/km (ida e volta), corridas até 40km: R$44 fixo, HP R$17, pedágios pagos.",
#         "requisitos": "Necessário EAR na CNH, MEI/CNPJ, veículo até 12 anos, ar-condicionado, CRLV, conta bancária/PIX, seguro do app, antecedentes.",
#         "seguro": "O seguro é obrigatório, cobre até R$100 mil, valor anual R$200 (R$100 pagos pelo parceiro).",
#         "documentos": "É preciso enviar: CNH, CRLV, dados bancários, chave PIX, MEI, 4 fotos do veículo, endereço, antecedentes criminais.",
#         "empresa": "A ATENTIVA é líder em transporte de segurados, fundada em 2013, 5 estrelas no Google, estrutura 24h.",
#     }
#     for k in keywords:
#         if k in question.lower():
#             return keywords[k]
#     return FAQ_TEXT

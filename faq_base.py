"""
Base de perguntas e respostas (FAQ) para o Agente Atentiva.

Este módulo concentra o conhecimento necessário para responder às
principais dúvidas dos candidatos a parceiros da ATENTIVA. Ele foi
construído a partir dos documentos de requisitos do projeto e do
retorno do cliente, contendo perguntas frequentes e respostas
humanizadas. Para tornar o sistema mais flexível, utiliza técnicas
simples de correspondência textual para encontrar a melhor resposta
mesmo quando o usuário escreve de forma diferente da pergunta
original.

Principais funcionalidades:
    * ``get_faq_answer``: recebe uma pergunta livre do usuário e
      retorna uma resposta humanizada, baseada em perguntas
      frequentes ou, se não houver correspondência, uma resposta
      padrão indicando contato com suporte humano.

Dependências:
    * scikit‑learn (sklearn) para vetorização TF‑IDF e cálculo de
      similaridade de cosseno.
"""

from __future__ import annotations

import random
import re
import unicodedata
from typing import List, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _normalize(text: str) -> str:
    """Remove acentuação e pontuação, e converte para minúsculas.

    Esta função facilita a comparação de strings em português, já que
    algumas entradas podem vir com ou sem acentos. Ela também
    substitui múltiplos espaços por um único espaço.
    """
    if not text:
        return ""
    # remove acentos
    nfkd_form = unicodedata.normalize("NFD", text)
    text = "".join([c for c in nfkd_form if unicodedata.category(c) != "Mn"])
    # remove pontuação e números
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    # converte para minúsculas
    text = text.lower()
    # normaliza espaços em branco
    text = " ".join(text.split())
    return text


# Lista de perguntas frequentes e suas respostas. Cada entrada possui
# "pergunta" com a formulação principal e "resposta" com o texto que
# será devolvido ao usuário. As perguntas são normalizadas para
# garantir melhor correspondência via TF‑IDF.
_FAQ_ENTRIES = [
    {
        "pergunta": "sou obrigado a aceitar todas as corridas ou posso recusar as que nao forem boas para mim",
        "resposta": (
            "Não! Lembre‑se que você é um parceiro e prestador de serviços para a Atentiva, e você não tem obrigação "
            "de aceitar todas as corridas que forem enviadas para você. Fique à vontade para recusar quando não "
            "for conveniente."
        ),
    },
    {
        "pergunta": "apos enviar meus documentos quanto tempo para ficar pronto cadastro",
        "resposta": (
            "Após enviar todos os documentos solicitados e preencher os dados, levamos até 2 dias para validar "
            "as informações e liberar seu acesso."
        ),
    },
    {
        "pergunta": "vou ter algum aplicativo para baixar e receber as corridas",
        "resposta": (
            "Sim! Após seu cadastro ser ativado, enviaremos pelo WhatsApp todas as instruções para download, "
            "instalação e configuração do aplicativo em seu celular. Também informaremos o usuário e a senha "
            "para acessar."
        ),
    },
    {
        "pergunta": "o que sao hps",
        "resposta": (
            "HPs são horas paradas. Caso você chegue ao endereço de embarque do passageiro antes do guincho, "
            "é preciso avisar no chat do app que o guincho ainda não chegou. Nossa atendente solicitará as "
            "horas paradas para você junto à seguradora."
        ),
    },
    {
        "pergunta": "quantas corridas devo ter por dia sabe me dizer se tem demanda em minha regiao",
        "resposta": (
            "A demanda varia bastante, pois dependemos das solicitações das seguradoras e da disponibilidade dos "
            "parceiros. Costumamos dizer que quem fica mais tempo logado e disponível recebe mais corridas. "
            "Não há um número fixo de chamadas por dia, e a demanda pode variar de região para região."
        ),
    },
    {
        "pergunta": "posso ir conhecer o escritorio e fazer uma visita na empresa",
        "resposta": (
            "Sim, claro! Será um prazer recebê‑lo. Apenas pedimos que avise com antecedência, pois o gestor comercial "
            "pode não estar no escritório todos os dias. Assim garantimos que sua visita seja proveitosa e que você "
            "possa tomar um café conosco."
        ),
    },
    {
        "pergunta": "meu carro é alugado isso e algum problema",
        "resposta": (
            "Não, veículos alugados são aceitos. Os requisitos principais são: o veículo não pode ultrapassar 12 anos "
            "de uso, precisa ter 4 portas e ar‑condicionado gelando, deve estar limpo e bem cuidado e, se tiver rodas "
            "de ferro, é necessário utilizar calotas."
        ),
    },
    {
        "pergunta": "meu carro e gnv isso e um problema ou pode ser cadastrado",
        "resposta": (
            "Infelizmente, veículos com GNV não são aceitos porque os cilindros geralmente ocupam o porta‑malas, "
            "o que dificulta o transporte das bagagens dos segurados."
        ),
    },
    {
        "pergunta": "como atentiva paga as corridas",
        "resposta": (
            "A remuneração é de R$ 44,00 para corridas que, somando ida e volta, não ultrapassem 40 km. Para distâncias "
            "maiores, pagamos R$ 1,10 por quilômetro rodado, sempre considerando ida e volta. Pedágios são reembolsados "
            "e há um adicional de R$ 80,00 para cada 1 000 km rodados. Horas paradas (HPs) também são remuneradas."
        ),
    },
    {
        "pergunta": "meu carro ja tem seguro eu tenho que fazer o seguro da atentiva",
        "resposta": (
            "Sim. A Atentiva trabalha com uma apólice de seguro corporativo exigida pelas seguradoras. Ela cobre o "
            "passageiro e o motorista em caso de acidentes. Mesmo que você já tenha seguro, é obrigatório aderir ao "
            "seguro da Atentiva, pois ele garante cobertura adequada ao serviço prestado."
        ),
    },
    {
        "pergunta": "o que a atentiva faz qual e o principal servico da atentiva",
        "resposta": (
            "A Atentiva é uma empresa especializada em transporte de segurados. Desde 2013, com sede em Sumaré/SP, a "
            "empresa transporta pessoas que possuem apólice de seguro veicular quando seus veículos ficam imobilizados "
            "por pane, batida ou sinistro."
        ),
    },
    {
        "pergunta": "quais sao os requisitos para se tornar parceiro quais sao os requisitos do motorista ou do veiculo",
        "resposta": (
            "Para se tornar parceiro, é necessário possuir CNH com a observação EAR (ou regularizar em até 12 dias), "
            "certidão de antecedentes criminais, MEI ou CNPJ para emissão de nota fiscal (é possível iniciar como "
            "pessoa física), conta bancária e chave PIX, e veículo com até 12 anos, quatro portas, ar‑condicionado "
            "funcionando, limpo, bem conservado e com CRLV em dia."
        ),
    },
    {
        "pergunta": "como funciona o cadastro quais documentos preciso enviar",
        "resposta": (
            "Após ler a apresentação e confirmar interesse, o próximo passo é enviar os documentos: CNH digital, "
            "CRLV digital, dados bancários, chave PIX da mesma conta, certificado MEI ou CNPJ, quatro fotos atuais do "
            "veículo, comprovante de endereço e atestado de antecedentes criminais. Após o envio, a validação leva "
            "até dois dias."
        ),
    },
    {
        "pergunta": "posso trabalhar com outros aplicativos a atentiva exige exclusividade",
        "resposta": (
            "A Atentiva não exige exclusividade. Você pode trabalhar com outros aplicativos de transporte. Apenas "
            "solicitamos que, quando estiver logado na nossa plataforma, esteja realmente disponível para realizar as "
            "corridas solicitadas."
        ),
    },
]


# Pré‑processamento: Vetorização das perguntas
# Como o scikit‑learn não possui uma lista nativa de stopwords em
# português nesta versão, não especificamos "stop_words" para evitar
# erro de carregamento. A vetorização funcionará sem remoção de
# palavras comuns. Caso queira adicionar stopwords manualmente, passe
# uma lista no parâmetro ``stop_words``.
_vectorizer = TfidfVectorizer()
_faq_questions_normalized = [_normalize(entry["pergunta"]) for entry in _FAQ_ENTRIES]
_faq_matrix = _vectorizer.fit_transform(_faq_questions_normalized)


def _personalize(answer: str) -> str:
    """Enriquece a resposta com um tom mais humano.

    Esta função adiciona uma saudação e um encerramento à resposta para
    suavizar o tom mecânico. Ela seleciona aleatoriamente entre algumas
    opções de preâmbulo e de encerramento para dar variedade às
    respostas.
    """
    prefaces = [
        "Claro!",
        "Com certeza!",
        "Sem problemas,",
        "Vamos lá:",
        "Ótima pergunta!",
    ]
    closings = [
        "Se precisar de mais alguma coisa, estou à disposição.",
        "Fique à vontade para perguntar caso surja outra dúvida.",
        "Conte comigo para o que precisar.",
    ]
    preface = random.choice(prefaces)
    closing = random.choice(closings)
    # Garante espaçamento adequado
    return f"{preface} {answer} {closing}"


def _match_faq(question: str) -> Optional[str]:
    """Procura a melhor correspondência para a pergunta no FAQ.

    Utiliza a similaridade de cosseno entre o vetor TF‑IDF da
    pergunta normalizada e a matriz das perguntas frequentes. Retorna
    a resposta correspondente se a similaridade máxima for acima de
    0.3, caso contrário retorna ``None``.
    """
    normalized_q = _normalize(question)
    if not normalized_q:
        return None
    q_vec = _vectorizer.transform([normalized_q])
    similarities = cosine_similarity(q_vec, _faq_matrix).flatten()
    best_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_idx])
    if best_score >= 0.3:
        return _FAQ_ENTRIES[best_idx]["resposta"]
    return None


def get_faq_answer(question: str) -> str:
    """Retorna uma resposta humanizada para a pergunta fornecida.

    Este é o ponto de entrada principal para o módulo. Ele tenta
    encontrar uma resposta no FAQ pré‑definido. Se encontrar, aplica
    uma camada de personalização e devolve. Caso contrário, retorna
    uma mensagem padrão sugerindo contato com um atendente humano.

    Parâmetros
    ----------
    question : str
        Pergunta formulada pelo usuário.

    Retorno
    -------
    str
        Resposta apropriada ou mensagem de fallback.
    """
    if not question or not question.strip():
        return "Por favor, digite sua dúvida para que eu possa ajudar."
    # Tenta obter resposta do FAQ
    answer = _match_faq(question)
    if answer:
        return _personalize(answer)
    # Resposta padrão
    return (
        "Ainda não possuo essa informação em minha base. Sugiro consultar "
        "a apresentação enviada ou entrar em contato diretamente com o "
        "Ricardo pelo número 19 99686‑8581 para um esclarecimento mais "
        "detalhado."
    )

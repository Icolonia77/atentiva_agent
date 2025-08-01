# utils.py

# Lista de cidades com apresentação específica de SP, baseada na distância de 45km da capital
# Fonte: Documento "Etapas Agente Atentiva", seção "Etapa 2"
CIDADES_SP_CAPITAL = [
    'aruja', 'barueri', 'caieiras', 'carapicuiba', 'cotia', 'diadema', 
    'embu das artes', 'ferraz de vasconcelos', 'franco da rocha', 'guarulhos', 
    'itapecerica da serra', 'itapevi', 'itaquaquecetuba', 'jandira', 
    'mairipora', 'osasco', 'ribeirao pires', 'santana de parnaiba', 
    'santo andre', 'sao bernardo do campo', 'sao caetano do sul', 'taboao da serra', 
    'vargem grande paulista'
]

def normalizar_texto(texto):
    """Remove acentos e converte para minúsculas para comparação."""
    if not isinstance(texto, str):
        return ""
    # Mapeamento de normalização para remover acentos
    return texto.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ç', 'c').replace('ã', 'a').replace('ô', 'o')

def get_presentation_by_city(cidade, estado):
    """
    Determina qual PDF de apresentação usar com base na cidade e estado.
    A função agora aceita dois argumentos para alinhar com main.py.
    """
    cidade_normalizada = normalizar_texto(cidade)
    estado_normalizado = estado.upper()

    # Se a cidade está na lista especial E o estado é São Paulo, retorna o PDF de SP
    if estado_normalizado == 'SP' and cidade_normalizada in CIDADES_SP_CAPITAL:
        return "PARCEIRO_ATENTIVA_SP.pdf"
    
    # Para todas as outras cidades de SP ou qualquer cidade de MG, retorna o PDF D7
    elif estado_normalizado in ['SP', 'MG']:
        return "PARCEIRO_ATENTIVA_D7.pdf"
    
    # Retorna None se a região não for suportada
    else:
        return None





# # utils.py

# CIDADES_SP_CAPITAL = [
#     'aruja', 'barueri', 'caieiras', 'carapicuiba', 'cotia', 'diadema',
#     'embu das artes', 'ferraz de vasconcelos', 'franco da rocha', 'guarulhos',
#     'itapecerica da serra', 'itapevi', 'itaquaquecetuba', 'jandira',
#     'mairipora', 'osasco', 'ribeirao pires', 'santana de parnaiba',
#     'santo andre', 'sao bernardo do campo', 'sao caetano do sul', 'taboao da serra',
#     'vargem grande paulista'
# ]

# def normalizar_texto(texto):
#     """Remove acentos e converte para minúsculas para comparação."""
#     if not isinstance(texto, str):
#         return ""
#     return texto.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ç', 'c').replace('ã', 'a').replace('ô', 'o')

# def get_presentation_by_city(city_state_string):
#     """Determina qual PDF de apresentação usar com base na cidade."""
#     cidade_normalizada = normalizar_texto(city_state_string.split(',')[0].strip())

#     if cidade_normalizada in CIDADES_SP_CAPITAL:
#         return "PARCEIRO_ATENTIVA_SP.pdf"
#     else:
#         return "PARCEIRO_ATENTIVA_D7.pdf"




# utils.py

# CIDADES_SP_45KM = [
#     "Arujá", "Barueri", "Caieiras", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes",
#     "Ferraz de Vasconcelos", "Franco da Rocha", "Guarulhos", "Itapecerica da Serra", "Itapevi",
#     "Itaquaquecetuba", "Jandira", "Mairiporã", "Osasco", "Ribeirão Pires", "Santana de Parnaíba",
#     "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "Taboão da Serra", "Vargem Grande Paulista"
# ]

# def get_presentation_by_city(city, state):
#     if state.upper() == "SP":
#         if city.title() in CIDADES_SP_45KM:
#             return "presentations/parceiro_atentiva_sp.pdf"
#         else:
#             return "presentations/parceiro_atentiva_d7.pdf"
#     elif state.upper() == "MG":
#         return "presentations/parceiro_atentiva_d7.pdf"
#     return None

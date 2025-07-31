# utils.py

CIDADES_SP_45KM = [
    "Arujá", "Barueri", "Caieiras", "Carapicuíba", "Cotia", "Diadema", "Embu das Artes",
    "Ferraz de Vasconcelos", "Franco da Rocha", "Guarulhos", "Itapecerica da Serra", "Itapevi",
    "Itaquaquecetuba", "Jandira", "Mairiporã", "Osasco", "Ribeirão Pires", "Santana de Parnaíba",
    "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "Taboão da Serra", "Vargem Grande Paulista"
]

def get_presentation_by_city(city, state):
    if state.upper() == "SP":
        if city.title() in CIDADES_SP_45KM:
            return "presentations/parceiro_atentiva_sp.pdf"
        else:
            return "presentations/parceiro_atentiva_d7.pdf"
    elif state.upper() == "MG":
        return "presentations/parceiro_atentiva_d7.pdf"
    return None

"""
Módulo de utilidades específico do agente Atentiva.

Este arquivo concentra a lógica para selecionar a apresentação em PDF
adequada com base na cidade e estado informados pelo lead. Para
evitar conflitos com módulos externos chamados ``utils``, escolhemos
um nome exclusivo (``atentiva_utils``). Assim garantimos que a
importação deste módulo sempre utilizará o código aqui definido.

As regras de seleção foram estabelecidas conforme o documento
"Etapas Agente Atentiva 20250719.docx" e revisadas pela equipe da
Atentiva:

    * Se o estado for São Paulo (``SP``) e a cidade estiver na lista
      de municípios até 45 km da capital, enviar a apresentação
      ``PARCEIRO_ATENTIVA_SP.pdf``.
    * Se a cidade estiver em qualquer lugar de São Paulo (fora da
      lista) ou em Minas Gerais (``MG``), enviar a apresentação
      ``PARCEIRO_ATENTIVA_D7.pdf``.
    * Caso contrário, retornar ``None`` para que o chamador possa
      tratar a situação de forma personalizada.

Os PDFs devem ser colocados no subdiretório ``documentos`` dentro
do diretório onde este módulo está localizado.
"""

from __future__ import annotations

import os
from typing import Optional


# Lista de cidades de SP que recebem a apresentação específica da capital
CIDADES_SP_CAPITAL = [
    "Arujá",
    "Barueri",
    "Caieiras",
    "Carapicuíba",
    "Cotia",
    "Diadema",
    "Embu das Artes",
    "Ferraz de Vasconcelos",
    "Franco da Rocha",
    "Guarulhos",
    "Itapecerica da Serra",
    "Itapevi",
    "Itaquaquecetuba",
    "Jandira",
    "Mairiporã",
    "Osasco",
    "Ribeirão Pires",
    "Santana de Parnaíba",
    "Santo André",
    "São Bernardo do Campo",
    "São Caetano do Sul",
    "Taboão da Serra",
    "Vargem Grande Paulista",
]


def get_presentation_by_city(cidade: str, estado: str) -> Optional[str]:
    """Determina o caminho da apresentação a partir da cidade e do estado.

    Parâmetros
    ----------
    cidade : str
        Cidade informada pelo lead.
    estado : str
        Estado (sigla) informado pelo lead.

    Retorno
    -------
    Optional[str]
        Caminho absoluto para o arquivo PDF apropriado ou ``None`` caso
        não haja apresentação disponível para a região.
    """
    if not cidade or not estado:
        return None

    cidade_normalizada = cidade.strip().title()
    estado_normalizado = estado.strip().upper()

    # Diretório base onde os PDFs devem estar
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_dir = os.path.join(base_dir, "documentos")

    # Seleção de apresentação
    if estado_normalizado == "SP" and cidade_normalizada in CIDADES_SP_CAPITAL:
        return os.path.join(pdf_dir, "PARCEIRO_ATENTIVA_SP.pdf")
    if estado_normalizado in {"SP", "MG"}:
        return os.path.join(pdf_dir, "PARCEIRO_ATENTIVA_D7.pdf")
    # Para demais estados/cidades, nenhuma apresentação disponível
    return None

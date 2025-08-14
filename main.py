# main.py
# VERSÃO CORRIGIDA

import streamlit as st
import os
from faq_base import get_faq_answer

# Vamos carregar a função utilitária no momento de uso. Isso permite
# recarregar o módulo em tempo de execução caso o arquivo utils.py
# seja atualizado sem reiniciar o servidor.
import importlib
import atentiva_utils as utils_module

st.set_page_config(page_title="Agente Atentiva", page_icon="🚗", layout="centered")

st.title("🤖 Agente Virtual - Atentiva Transportes Executivos")

if 'etapa' not in st.session_state:
    st.session_state.etapa = 1
if 'lead_data' not in st.session_state:
    st.session_state.lead_data = {}
if 'faq_submit' not in st.session_state:
    st.session_state.faq_submit = False
if 'faq_input_cache' not in st.session_state:
    st.session_state.faq_input_cache = ""

def next_step():
    st.session_state.etapa += 1

def restart():
    st.session_state.etapa = 1
    st.session_state.lead_data = {}
    st.session_state.faq_submit = False
    st.session_state.faq_input_cache = ""

st.sidebar.button("🔁 Voltar ao Início", on_click=restart)

# Etapa 1: Qualificação Inicial
if st.session_state.etapa == 1:
    st.info("Olá! Que bom ver seu interesse em se tornar um parceiro da Atentiva Transportes. Vou te ajudar nos primeiros passos, ok? Responda algumas perguntas rápidas!")
    nome = st.text_input("Qual seu nome completo?", key="nome_input")
    if st.button("Próximo", key="btn1"):
        if nome.strip():
            st.session_state.lead_data['nome'] = nome
            next_step()
            st.rerun()
        else:
            st.warning("Por favor, preencha seu nome antes de continuar.")

# Etapa 2: Cidade/Estado
elif st.session_state.etapa == 2:
    cidade = st.text_input("Qual sua cidade?", key="cidade_input")
    estado = st.text_input("Qual seu estado (sigla)?", key="estado_input")
    if st.button("Próximo", key="btn2"):
        if cidade.strip() and estado.strip():
            st.session_state.lead_data['cidade'] = cidade
            st.session_state.lead_data['estado'] = estado.upper()
            next_step()
            st.rerun()
        else:
            st.warning("Preencha cidade e estado antes de continuar.")

# Etapa 3: Experiência
elif st.session_state.etapa == 3:
    experiencia = st.radio("Já possui experiência com aplicativos de transporte (Uber, 99, etc.)?", ["Sim", "Não"], key="exp_radio")
    tempo_exp = ""
    if experiencia == "Sim":
        tempo_exp = st.text_input("Se sim, há quanto tempo?", key="tempo_exp_input")
    modelo = st.text_input("Qual o modelo e ano do seu veículo?", key="modelo_input")
    ar_cond = st.radio("O veículo possui ar-condicionado?", ["Sim", "Não"], key="ar_cond_radio")
    cnh = st.radio("Sua CNH está válida e possui a observação EAR?", ["Sim", "Não"], key="cnh_radio")
    mei = st.radio("Você possui um CNPJ MEI ativo?", ["Sim", "Não"], key="mei_radio")
    if st.button("Próximo", key="btn3"):
        if modelo.strip() and ar_cond and cnh and mei:
            st.session_state.lead_data['experiencia'] = experiencia
            st.session_state.lead_data['tempo_exp'] = tempo_exp
            st.session_state.lead_data['modelo'] = modelo
            st.session_state.lead_data['ar_cond'] = ar_cond
            st.session_state.lead_data['cnh_ear'] = cnh
            st.session_state.lead_data['mei'] = mei
            next_step()
            st.rerun()
        else:
            st.warning("Preencha todos os campos obrigatórios para prosseguir.")

# Etapa 4: Apresentação Personalizada
elif st.session_state.etapa == 4:
    cidade = st.session_state.lead_data.get('cidade', '')
    estado = st.session_state.lead_data.get('estado', '')
    # Recarregamos o módulo utils para garantir que modificações no arquivo
    # utils.py sejam refletidas imediatamente. Assim evitamos a necessidade
    # de reiniciar o servidor sempre que a lógica de seleção de PDFs for
    # atualizada.
    utils_module = importlib.reload(utils_module)
    doc_path = utils_module.get_presentation_by_city(cidade, estado)
    if doc_path:
        st.success(
            f"Aqui está a apresentação do parceiro Atentiva para {cidade}/{estado}. "
            "Ela contém detalhes importantes sobre o trabalho, remuneração e requisitos. "
            "Faça o download, leia com calma e depois confirme a leitura para seguirmos."
        )
        with open(doc_path, "rb") as file:
            st.download_button(
                "📄 Baixar Apresentação",
                data=file,
                file_name=os.path.basename(doc_path),
            )
        lido = st.radio(
            "Você conseguiu ler a apresentação por completo?",
            ["Sim", "Ainda não"],
            key="apresent_radio",
        )
        if st.button("Próximo", key="btn4"):
            if lido == "Sim":
                next_step()
                st.rerun()
            else:
                st.warning(
                    "Sem problemas! Leia a apresentação com atenção e confirme a leitura para prosseguir."
                )
    else:
        st.warning(
            "Ops! Ainda não atendemos sua região ou não temos uma apresentação específica. "
            "Por favor, entre em contato com o Ricardo (19 99686‑8581) para verificarmos a melhor forma de prosseguir."
        )

# Etapa 5: Upload dos Documentos
elif st.session_state.etapa == 5:
    st.header("Envio de Documentos para Cadastro")
    st.markdown(
        '''
        Estamos quase lá! Para concluir seu cadastro, precisamos dos seguintes documentos:

        - **Foto da CNH** (preferencialmente versão digital em PDF)
        - **Foto do CRLV** (preferencialmente versão digital em PDF)
        - **Dados Bancários** (Banco / Agência / Conta / Corrente ou Poupança / Nome Titular / CPF ou CNPJ)
        - **Chave PIX** (deve ser da mesma conta informada acima)
        - **Certificado MEI** (ou apenas informe o CNPJ)
        - **4 fotos atuais do veículo** (frente, traseira e laterais)
        - **Endereço completo e CEP**
        - **Atestado de Antecedentes Criminais**

        Você pode anexar arquivos nos formatos PDF, JPG ou PNG. Envie todos os documentos de uma só vez para facilitar nossa análise.
        '''
    )
    files = st.file_uploader(
        "Clique ou arraste os arquivos aqui",
        accept_multiple_files=True,
        type=["pdf", "jpg", "jpeg", "png"],
    )
    endereco = st.text_area("Endereço completo e CEP", key="endereco_input")
    dados_bancarios = st.text_area(
        "Dados Bancários (Banco, Agência, Conta, Corrente ou Poupança, Nome Titular, CPF ou CNPJ)",
        key="dados_bancarios_input",
    )
    chave_pix = st.text_input(
        "Chave PIX (deve ser da mesma conta bancária informada)",
        key="chave_pix_input",
    )
    if st.button("Enviar Documentos", key="btn5"):
        if files and endereco.strip() and dados_bancarios.strip() and chave_pix.strip():
            st.session_state.lead_data["docs"] = [f.name for f in files]
            st.session_state.lead_data["endereco"] = endereco
            st.session_state.lead_data["dados_bancarios"] = dados_bancarios
            st.session_state.lead_data["chave_pix"] = chave_pix
            next_step()
            st.rerun()
        else:
            st.warning(
                "Por favor, preencha todos os campos e anexe os arquivos solicitados antes de prosseguir."
            )

# Etapa 6: Boas‑vindas e próximos passos
elif st.session_state.etapa == 6:
    st.success(
        "Recebemos todos os seus documentos e iniciaremos a análise agora mesmo! "
        "Em até 2 dias úteis você receberá seu acesso ao treinamento e ao aplicativo. "
        "Qualquer dúvida nesse período, é só chamar o Ricardo no WhatsApp 19 99686‑8581."
    )
    if st.button("Reiniciar"):
        restart()
        st.rerun()

st.divider()
st.subheader("❓ Dúvidas sobre a Atentiva? Pergunte abaixo:")

faq_input = st.text_input("Digite sua dúvida sobre a Atentiva:", key="faq_input")
faq_submitted = st.button("Enviar Pergunta", key="faq_btn")

if faq_submitted:
    st.session_state.faq_submit = True
    st.session_state.faq_input_cache = faq_input
elif not faq_input:
    st.session_state.faq_submit = False
    st.session_state.faq_input_cache = ""

if st.session_state.faq_submit and st.session_state.faq_input_cache:
    st.info(get_faq_answer(st.session_state.faq_input_cache))





# # main.py
# # NENHUMA ALTERAÇÃO NECESSÁRIA AQUI. O CÓDIGO ESTÁ CORRETO.

# import streamlit as st
# from utils import get_presentation_by_city
# from faq_base import get_faq_answer

# st.set_page_config(page_title="Agente Atentiva", page_icon="🚗", layout="centered")

# st.title("🤖 Agente Virtual - Atentiva Transportes Executivos")

# if 'etapa' not in st.session_state:
#     st.session_state.etapa = 1
# if 'lead_data' not in st.session_state:
#     st.session_state.lead_data = {}
# if 'faq_submit' not in st.session_state:
#     st.session_state.faq_submit = False
# if 'faq_input_cache' not in st.session_state:
#     st.session_state.faq_input_cache = ""

# def next_step():
#     st.session_state.etapa += 1

# def restart():
#     st.session_state.etapa = 1
#     st.session_state.lead_data = {}
#     st.session_state.faq_submit = False
#     st.session_state.faq_input_cache = ""

# st.sidebar.button("🔁 Voltar ao Início", on_click=restart)

# # Etapa 1: Qualificação Inicial
# if st.session_state.etapa == 1:
#     st.info("Olá! Que bom ver seu interesse em se tornar um parceiro da Atentiva Transportes. Vou te ajudar nos primeiros passos, ok? Responda algumas perguntas rápidas!")
#     nome = st.text_input("Qual seu nome completo?", key="nome_input")
#     if st.button("Próximo", key="btn1"):
#         if nome.strip():
#             st.session_state.lead_data['nome'] = nome
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Por favor, preencha seu nome antes de continuar.")

# # Etapa 2: Cidade/Estado
# elif st.session_state.etapa == 2:
#     cidade = st.text_input("Qual sua cidade?", key="cidade_input")
#     estado = st.text_input("Qual seu estado (sigla)?", key="estado_input")
#     if st.button("Próximo", key="btn2"):
#         if cidade.strip() and estado.strip():
#             st.session_state.lead_data['cidade'] = cidade
#             st.session_state.lead_data['estado'] = estado.upper()
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Preencha cidade e estado antes de continuar.")

# # Etapa 3: Experiência
# elif st.session_state.etapa == 3:
#     experiencia = st.radio("Já possui experiência com aplicativos de transporte (Uber, 99, etc.)?", ["Sim", "Não"], key="exp_radio")
#     tempo_exp = ""
#     if experiencia == "Sim":
#         tempo_exp = st.text_input("Se sim, há quanto tempo?", key="tempo_exp_input")
#     modelo = st.text_input("Qual o modelo e ano do seu veículo?", key="modelo_input")
#     ar_cond = st.radio("O veículo possui ar-condicionado?", ["Sim", "Não"], key="ar_cond_radio")
#     cnh = st.radio("Sua CNH está válida e possui a observação EAR?", ["Sim", "Não"], key="cnh_radio")
#     mei = st.radio("Você possui um CNPJ MEI ativo?", ["Sim", "Não"], key="mei_radio")
#     if st.button("Próximo", key="btn3"):
#         if modelo.strip() and ar_cond and cnh and mei:
#             st.session_state.lead_data['experiencia'] = experiencia
#             st.session_state.lead_data['tempo_exp'] = tempo_exp
#             st.session_state.lead_data['modelo'] = modelo
#             st.session_state.lead_data['ar_cond'] = ar_cond
#             st.session_state.lead_data['cnh_ear'] = cnh
#             st.session_state.lead_data['mei'] = mei
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Preencha todos os campos obrigatórios para prosseguir.")

# # Etapa 4: Apresentação Personalizada
# elif st.session_state.etapa == 4:
#     cidade = st.session_state.lead_data.get('cidade', '')
#     estado = st.session_state.lead_data.get('estado', '')
#     doc_path = get_presentation_by_city(cidade, estado)
#     if doc_path:
#         st.success(f"Baixe e leia a apresentação do parceiro Atentiva para sua região ({cidade}/{estado}):")
#         with open(doc_path, "rb") as file:
#             st.download_button("📄 Baixar Apresentação", data=file, file_name=doc_path)
#         lido = st.radio("Leu a apresentação completa?", ["Sim", "Ainda não"], key="apresent_radio")
#         if st.button("Próximo", key="btn4"):
#             if lido == "Sim":
#                 next_step()
#                 st.rerun()
#             else:
#                 st.warning("Por favor, confirme a leitura da apresentação para prosseguir.")
#     else:
#         st.warning("Região não suportada no momento. Entre em contato com Ricardo (19 99686-8581).")

# # Etapa 5: Upload dos Documentos
# elif st.session_state.etapa == 5:
#     st.header("Envio de Documentos para Cadastro")
#     st.markdown("""
#     - **Foto da CNH** (preferencialmente PDF) 
#     - **Foto do CRLV** (preferencialmente PDF) 
#     - **Dados Bancários** (Banco / Agência / Conta / Tipo / Nome / CPF ou CNPJ) 
#     - **Chave PIX** 
#     - **Certificado MEI** 
#     - **4 fotos atuais do veículo** (frente, trás, laterais) 
#     - **Endereço completo e CEP** 
#     - **Atestado de Antecedentes Criminais** 
#     """)
#     files = st.file_uploader("Envie todos os arquivos aqui (PDF, JPG ou PNG)", accept_multiple_files=True, type=["pdf","jpg","jpeg","png"])
#     endereco = st.text_area("Endereço completo e CEP", key="endereco_input")
#     dados_bancarios = st.text_area("Dados Bancários (Banco, Agência, Conta, Tipo, Nome, CPF ou CNPJ)", key="dados_bancarios_input")
#     chave_pix = st.text_input("Chave PIX", key="chave_pix_input")
#     if st.button("Enviar Documentos", key="btn5"):
#         if files and endereco.strip() and dados_bancarios.strip() and chave_pix.strip():
#             st.session_state.lead_data['docs'] = [f.name for f in files]
#             st.session_state.lead_data['endereco'] = endereco
#             st.session_state.lead_data['dados_bancarios'] = dados_bancarios
#             st.session_state.lead_data['chave_pix'] = chave_pix
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Preencha todos os campos e envie os arquivos para prosseguir.")

# # Etapa 6: Boas-vindas e próximos passos
# elif st.session_state.etapa == 6:
#     st.success("Documentos recebidos! Agora é só aguardar a validação e liberar seu treinamento. Dúvidas? [cite_start]Chame Ricardo no WhatsApp 19 99686-8581.") [cite: 56, 62]
#     if st.button("Reiniciar"):
#         restart()
#         st.rerun()

# st.divider()
# st.subheader("❓ Dúvidas sobre a Atentiva? Pergunte abaixo:")

# faq_input = st.text_input("Digite sua dúvida sobre a Atentiva:", key="faq_input")
# faq_submitted = st.button("Enviar Pergunta", key="faq_btn")

# if faq_submitted:
#     st.session_state.faq_submit = True
#     st.session_state.faq_input_cache = faq_input
# elif not faq_input:
#     st.session_state.faq_submit = False
#     st.session_state.faq_input_cache = ""

# if st.session_state.faq_submit and st.session_state.faq_input_cache:
#     st.info(get_faq_answer(st.session_state.faq_input_cache))


# # main.py

# import streamlit as st
# from utils import get_presentation_by_city
# from faq_base import get_faq_answer

# st.set_page_config(page_title="Agente Atentiva", page_icon="🚗", layout="centered")

# st.title("🤖 Agente Virtual - Atentiva Transportes Executivos")

# if 'etapa' not in st.session_state:
#     st.session_state.etapa = 1
# if 'lead_data' not in st.session_state:
#     st.session_state.lead_data = {}
# if 'faq_submit' not in st.session_state:
#     st.session_state.faq_submit = False
# if 'faq_input_cache' not in st.session_state:
#     st.session_state.faq_input_cache = ""

# def next_step():
#     st.session_state.etapa += 1

# def restart():
#     st.session_state.etapa = 1
#     st.session_state.lead_data = {}
#     st.session_state.faq_submit = False
#     st.session_state.faq_input_cache = ""

# # Botão sempre visível para voltar ao início
# st.sidebar.button("🔁 Voltar ao Início", on_click=restart)
# # Ou, se quiser o botão centralizado na página, pode deixar assim:
# # if st.button("🔁 Voltar ao Início (página inicial)"):
# #     restart()
# #     st.rerun()

# # Etapa 1: Qualificação Inicial
# if st.session_state.etapa == 1:
#     st.info("Olá! Que bom ver seu interesse em se tornar um parceiro da Atentiva Transportes. Vou te ajudar nos primeiros passos, ok? Responda algumas perguntas rápidas!")
#     nome = st.text_input("Qual seu nome completo?", key="nome_input")
#     if st.button("Próximo", key="btn1"):
#         if nome.strip():
#             st.session_state.lead_data['nome'] = nome
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Por favor, preencha seu nome antes de continuar.")

# # Etapa 2: Cidade/Estado
# elif st.session_state.etapa == 2:
#     cidade = st.text_input("Qual sua cidade?", key="cidade_input")
#     estado = st.text_input("Qual seu estado (sigla)?", key="estado_input")
#     if st.button("Próximo", key="btn2"):
#         if cidade.strip() and estado.strip():
#             st.session_state.lead_data['cidade'] = cidade
#             st.session_state.lead_data['estado'] = estado.upper()
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Preencha cidade e estado antes de continuar.")

# # Etapa 3: Experiência
# elif st.session_state.etapa == 3:
#     experiencia = st.radio("Já possui experiência com aplicativos de transporte (Uber, 99, etc.)?", ["Sim", "Não"], key="exp_radio")
#     tempo_exp = ""
#     if experiencia == "Sim":
#         tempo_exp = st.text_input("Se sim, há quanto tempo?", key="tempo_exp_input")
#     modelo = st.text_input("Qual o modelo e ano do seu veículo?", key="modelo_input")
#     ar_cond = st.radio("O veículo possui ar-condicionado?", ["Sim", "Não"], key="ar_cond_radio")
#     cnh = st.radio("Sua CNH está válida e possui a observação EAR?", ["Sim", "Não"], key="cnh_radio")
#     mei = st.radio("Você possui um CNPJ MEI ativo?", ["Sim", "Não"], key="mei_radio")
#     if st.button("Próximo", key="btn3"):
#         if modelo.strip() and ar_cond and cnh and mei:
#             st.session_state.lead_data['experiencia'] = experiencia
#             st.session_state.lead_data['tempo_exp'] = tempo_exp
#             st.session_state.lead_data['modelo'] = modelo
#             st.session_state.lead_data['ar_cond'] = ar_cond
#             st.session_state.lead_data['cnh_ear'] = cnh
#             st.session_state.lead_data['mei'] = mei
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Preencha todos os campos obrigatórios para prosseguir.")

# # Etapa 4: Apresentação Personalizada
# elif st.session_state.etapa == 4:
#     cidade = st.session_state.lead_data.get('cidade', '')
#     estado = st.session_state.lead_data.get('estado', '')
#     doc_path = get_presentation_by_city(cidade, estado)
#     if doc_path:
#         st.success(f"Baixe e leia a apresentação do parceiro Atentiva para sua região ({cidade}/{estado}):")
#         with open(doc_path, "rb") as file:
#             st.download_button("📄 Baixar Apresentação", data=file, file_name=doc_path.split("/")[-1])
#         lido = st.radio("Leu a apresentação completa?", ["Sim", "Ainda não"], key="apresent_radio")
#         if st.button("Próximo", key="btn4"):
#             if lido == "Sim":
#                 next_step()
#                 st.rerun()
#             else:
#                 st.warning("Por favor, confirme a leitura da apresentação para prosseguir.")
#     else:
#         st.warning("Região não suportada no momento. Entre em contato com Ricardo (19 99686-8581).")

# # Etapa 5: Upload dos Documentos
# elif st.session_state.etapa == 5:
#     st.header("Envio de Documentos para Cadastro")
#     st.markdown("""
#     - **Foto da CNH** (preferencialmente PDF)
#     - **Foto do CRLV** (preferencialmente PDF)
#     - **Dados Bancários** (Banco / Agência / Conta / Tipo / Nome / CPF ou CNPJ)
#     - **Chave PIX**
#     - **Certificado MEI**
#     - **4 fotos atuais do veículo** (frente, trás, laterais)
#     - **Endereço completo e CEP**
#     - **Atestado de Antecedentes Criminais**
#     """)
#     files = st.file_uploader("Envie todos os arquivos aqui (PDF, JPG ou PNG)", accept_multiple_files=True, type=["pdf","jpg","jpeg","png"])
#     endereco = st.text_area("Endereço completo e CEP", key="endereco_input")
#     dados_bancarios = st.text_area("Dados Bancários (Banco, Agência, Conta, Tipo, Nome, CPF ou CNPJ)", key="dados_bancarios_input")
#     chave_pix = st.text_input("Chave PIX", key="chave_pix_input")
#     if st.button("Enviar Documentos", key="btn5"):
#         if files and endereco.strip() and dados_bancarios.strip() and chave_pix.strip():
#             st.session_state.lead_data['docs'] = [f.name for f in files]
#             st.session_state.lead_data['endereco'] = endereco
#             st.session_state.lead_data['dados_bancarios'] = dados_bancarios
#             st.session_state.lead_data['chave_pix'] = chave_pix
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Preencha todos os campos e envie os arquivos para prosseguir.")

# # Etapa 6: Boas-vindas e próximos passos
# elif st.session_state.etapa == 6:
#     st.success("Documentos recebidos! Agora é só aguardar a validação e liberar seu treinamento. Dúvidas? Chame Ricardo no WhatsApp 19 99686-8581.")
#     if st.button("Reiniciar"):
#         restart()
#         st.rerun()

# st.divider()
# st.subheader("❓ Dúvidas sobre a Atentiva? Pergunte abaixo:")

# faq_input = st.text_input("Digite sua dúvida sobre a Atentiva:", key="faq_input")
# faq_submitted = st.button("Enviar Pergunta", key="faq_btn")

# if faq_submitted:
#     st.session_state.faq_submit = True
#     st.session_state.faq_input_cache = faq_input
# elif not faq_input:
#     st.session_state.faq_submit = False
#     st.session_state.faq_input_cache = ""

# if st.session_state.faq_submit and st.session_state.faq_input_cache:
#     st.info(get_faq_answer(st.session_state.faq_input_cache))



# # main.py

# import streamlit as st
# from utils import get_presentation_by_city
# from faq_base import get_faq_answer

# st.set_page_config(page_title="Agente Atentiva", page_icon="🚗", layout="centered")

# st.title("🤖 Agente Virtual - Atentiva Transportes Executivos")

# if 'etapa' not in st.session_state:
#     st.session_state.etapa = 1
# if 'lead_data' not in st.session_state:
#     st.session_state.lead_data = {}

# def next_step():
#     st.session_state.etapa += 1

# def restart():
#     st.session_state.etapa = 1
#     st.session_state.lead_data = {}

# # Etapa 1: Qualificação Inicial
# if st.session_state.etapa == 1:
#     st.info("Olá! Que bom ver seu interesse em se tornar um parceiro da Atentiva Transportes. Vou te ajudar nos primeiros passos, ok? Responda algumas perguntas rápidas!")
#     nome = st.text_input("Qual seu nome completo?", key="nome_input")
#     if st.button("Próximo", key="btn1"):
#         if nome.strip():
#             st.session_state.lead_data['nome'] = nome
#             next_step()
#             st.rerun()
#         else:
#             st.warning("Por favor, preencha seu nome antes de continuar.")

# # Etapa 2: Cidade/Estado
# elif st.session_state.etapa == 2:
#     cidade = st.text_input("Qual sua cidade?", key="cidade_input")
#     estado = st.text_input("Qual seu estado (sigla)?", key="estado_input")
#     if st.button("Próximo", key="btn2"):
#         if cidade.strip() and estado.strip():
#             st.session_state.lead_data['cidade'] = cidade
#             st.session_state.lead_data['estado'] = estado.upper()
#             next_step()
#             st.experimental_rerun()
#         else:
#             st.warning("Preencha cidade e estado antes de continuar.")

# # Etapa 3: Experiência
# elif st.session_state.etapa == 3:
#     experiencia = st.radio("Já possui experiência com aplicativos de transporte (Uber, 99, etc.)?", ["Sim", "Não"], key="exp_radio")
#     tempo_exp = ""
#     if experiencia == "Sim":
#         tempo_exp = st.text_input("Se sim, há quanto tempo?", key="tempo_exp_input")
#     modelo = st.text_input("Qual o modelo e ano do seu veículo?", key="modelo_input")
#     ar_cond = st.radio("O veículo possui ar-condicionado?", ["Sim", "Não"], key="ar_cond_radio")
#     cnh = st.radio("Sua CNH está válida e possui a observação EAR?", ["Sim", "Não"], key="cnh_radio")
#     mei = st.radio("Você possui um CNPJ MEI ativo?", ["Sim", "Não"], key="mei_radio")
#     if st.button("Próximo", key="btn3"):
#         if modelo.strip() and ar_cond and cnh and mei:
#             st.session_state.lead_data['experiencia'] = experiencia
#             st.session_state.lead_data['tempo_exp'] = tempo_exp
#             st.session_state.lead_data['modelo'] = modelo
#             st.session_state.lead_data['ar_cond'] = ar_cond
#             st.session_state.lead_data['cnh_ear'] = cnh
#             st.session_state.lead_data['mei'] = mei
#             next_step()
#             st.experimental_rerun()
#         else:
#             st.warning("Preencha todos os campos obrigatórios para prosseguir.")

# # Etapa 4: Apresentação Personalizada
# elif st.session_state.etapa == 4:
#     cidade = st.session_state.lead_data.get('cidade', '')
#     estado = st.session_state.lead_data.get('estado', '')
#     doc_path = get_presentation_by_city(cidade, estado)
#     if doc_path:
#         st.success(f"Baixe e leia a apresentação do parceiro Atentiva para sua região ({cidade}/{estado}):")
#         with open(doc_path, "rb") as file:
#             st.download_button("📄 Baixar Apresentação", data=file, file_name=doc_path.split("/")[-1])
#         lido = st.radio("Leu a apresentação completa?", ["Sim", "Ainda não"], key="apresent_radio")
#         if st.button("Próximo", key="btn4"):
#             if lido == "Sim":
#                 next_step()
#                 st.experimental_rerun()
#             else:
#                 st.warning("Por favor, confirme a leitura da apresentação para prosseguir.")
#     else:
#         st.warning("Região não suportada no momento. Entre em contato com Ricardo (19 99686-8581).")

# # Etapa 5: Upload dos Documentos
# elif st.session_state.etapa == 5:
#     st.header("Envio de Documentos para Cadastro")
#     st.markdown("""
#     - **Foto da CNH** (preferencialmente PDF)
#     - **Foto do CRLV** (preferencialmente PDF)
#     - **Dados Bancários** (Banco / Agência / Conta / Tipo / Nome / CPF ou CNPJ)
#     - **Chave PIX**
#     - **Certificado MEI**
#     - **4 fotos atuais do veículo** (frente, trás, laterais)
#     - **Endereço completo e CEP**
#     - **Atestado de Antecedentes Criminais**
#     """)
#     files = st.file_uploader("Envie todos os arquivos aqui (PDF, JPG ou PNG)", accept_multiple_files=True, type=["pdf","jpg","jpeg","png"])
#     endereco = st.text_area("Endereço completo e CEP", key="endereco_input")
#     dados_bancarios = st.text_area("Dados Bancários (Banco, Agência, Conta, Tipo, Nome, CPF ou CNPJ)", key="dados_bancarios_input")
#     chave_pix = st.text_input("Chave PIX", key="chave_pix_input")
#     if st.button("Enviar Documentos", key="btn5"):
#         if files and endereco.strip() and dados_bancarios.strip() and chave_pix.strip():
#             st.session_state.lead_data['docs'] = [f.name for f in files]
#             st.session_state.lead_data['endereco'] = endereco
#             st.session_state.lead_data['dados_bancarios'] = dados_bancarios
#             st.session_state.lead_data['chave_pix'] = chave_pix
#             next_step()
#             st.experimental_rerun()
#         else:
#             st.warning("Preencha todos os campos e envie os arquivos para prosseguir.")

# # Etapa 6: Boas-vindas e próximos passos
# elif st.session_state.etapa == 6:
#     st.success("Documentos recebidos! Agora é só aguardar a validação e liberar seu treinamento. Dúvidas? Chame Ricardo no WhatsApp 19 99686-8581.")
#     if st.button("Reiniciar"):
#         restart()
#         st.experimental_rerun()

# st.divider()
# st.subheader("❓ Dúvidas sobre a Atentiva? Pergunte abaixo:")
# faq_q = st.text_input("Digite sua dúvida sobre a Atentiva:", key="faq_input")
# if faq_q:
#     st.info(get_faq_answer(faq_q))


# main.py
import streamlit as st
from utils import get_presentation_by_city

# Lista de perguntas de qualificação
PERGUNTAS_QUALIFICACAO = [
    "Qual seu nome completo?",
    "Qual sua cidade e estado?",
    "Já possui experiência com aplicativos de transporte (Uber, 99, etc.)?",
    "Se sim, há quanto tempo?",
    "Qual o modelo e ano do seu veículo?",
    "Ele possui ar-condicionado?",
    "Sua CNH está válida e possui a observação EAR (Exerce Atividade Remunerada)?",
    "Você possui um CNPJ MEI ativo?"
]

def inicializar_estado():
    """Inicializa o estado da sessão se ainda não existir."""
    if 'etapa' not in st.session_state:
        st.session_state.etapa = "inicio"
        st.session_state.dados_lead = {}
        st.session_state.indice_pergunta = 0
        st.session_state.mensagens = []

def proxima_etapa(nome_etapa):
    """Avança para a próxima etapa do fluxo."""
    st.session_state.etapa = nome_etapa
    st.rerun()

def adicionar_mensagem(autor, texto):
    """Adiciona uma mensagem ao histórico do chat."""
    st.session_state.mensagens.append({"autor": autor, "texto": texto})

# --- LÓGICA PRINCIPAL DO AGENTE ---
st.set_page_config(page_title="Assistente de Cadastro Atentiva", layout="centered")
st.title("Assistente Virtual de Cadastro - Atentiva Transportes")
st.markdown("Olá! Sou o seu assistente para o processo de cadastro de parceiros.")

inicializar_estado()

# Exibe o histórico de mensagens
for msg in st.session_state.mensagens:
    with st.chat_message(msg["autor"]):
        st.write(msg["texto"])

if st.session_state.etapa == "inicio":
    if st.button("Olá! Quero iniciar meu cadastro"):
        mensagem_saudacao = "Olá! Que bom ver seu interesse em se tornar um parceiro da Atentiva Transportes. Eu sou o Agente Virtual Especialista em contratação de parceiro da Atentiva e vou te ajudar com os primeiros passos, ok? Para que eu possa te fornecer as informações corretas e personalizadas para a sua região, preciso que me responda algumas perguntas rápidas:"
        adicionar_mensagem("assistant", mensagem_saudacao)
        proxima_etapa("qualificacao")

elif st.session_state.etapa == "qualificacao":
    indice_atual = st.session_state.indice_pergunta
    
    if indice_atual < len(PERGUNTAS_QUALIFICACAO):
        pergunta_atual = PERGUNTAS_QUALIFICACAO[indice_atual]

        # Lógica para pular a pergunta condicional
        if pergunta_atual == "Se sim, há quanto tempo?":
            pergunta_anterior = "Já possui experiência com aplicativos de transporte (Uber, 99, etc.)?"
            resposta_experiencia = st.session_state.dados_lead.get(pergunta_anterior, "").lower()
            
            if 'nao' in resposta_experiencia or 'não' in resposta_experiencia:
                st.session_state.indice_pergunta += 1
                st.rerun()

        # Mostra o input se a pergunta não for pulada
        else:
            resposta = st.text_input(pergunta_atual, key=f"resposta_{indice_atual}")
            if st.button("Enviar Resposta", key=f"btn_{indice_atual}"):
                if resposta:
                    adicionar_mensagem("assistant", pergunta_atual)
                    adicionar_mensagem("user", resposta)
                    st.session_state.dados_lead[pergunta_atual] = resposta
                    st.session_state.indice_pergunta += 1
                    st.rerun()
                else:
                    st.warning("Por favor, forneça uma resposta.")
    else:
        # Finalizou as perguntas
        if not st.session_state.get('qualificacao_concluida', False):
             adicionar_mensagem("assistant", "Obrigado pelas respostas! A analisar a sua localização para personalizar o próximo passo...")
             st.session_state.qualificacao_concluida = True
             proxima_etapa("personalizacao")

elif st.session_state.etapa == "personalizacao":
    # Pega a string completa, como o utilizador a digitou
    cidade_estado_string = st.session_state.dados_lead.get("Qual sua cidade e estado?", "")
    
    # Passa a string COMPLETA para a função, como esperado
    pdf_filename = get_presentation_by_city(cidade_estado_string) 
    
    mensagem_documento = f"Com base na sua localização, a apresentação correta é a **{pdf_filename}**. Por favor, clique no botão abaixo para descarregar e ler o documento."
    adicionar_mensagem("assistant", mensagem_documento)

    try:
        with open(pdf_filename, "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Descarregar Apresentação",
                            data=PDFbyte,
                            file_name=pdf_filename,
                            mime='application/octet-stream')
    except FileNotFoundError:
        st.error(f"Erro: O ficheiro {pdf_filename} não foi encontrado. Verifique se ele foi enviado para o repositório no GitHub.")
    
    if st.button("Já li a apresentação e quero continuar"):
        proxima_etapa("solicitar_documentos")

elif st.session_state.etapa == "solicitar_documentos":
    # O código para esta etapa e a etapa de finalização permanece o mesmo
    mensagem_solicitacao = """
    Estamos quase lá! Mais alguns detalhes e você será um parceiro ATENTIVA.
    Como conversamos anteriormente e após ter enviado as respostas acima, agora preciso dos documentos abaixo para dar sequência em seu cadastro ok.

    **ENVIO DE DOCUMENTOS:**
    - ✅ Foto da sua CNH (PREFERENCIALMENTE CNH DIGITAL EM PDF).
    - ✅ Foto do CRLV do seu veículo (PREFERENCIALMENTE CRLV DIGITAL EM PDF).
    - ✅ Dados Bancários (Banco / Agência / Conta e Díg / Tipo da Conta / Nome do Titular / CPF).
    - ✅ Chave PIX da mesma conta informada acima.
    - ✅ Certificado MEI.
    - ✅ 4 fotos atuais dos 4 lados do veículo.
    - ✅ Endereço Completo e CEP.
    - ✅ Atestado de Antecedentes Criminais.

    *Nesta demonstração, clique no botão abaixo para simular o envio e avançar.*
    """
    adicionar_mensagem("assistant", mensagem_solicitacao)

    if st.button("Simular Envio de Documentos"):
        proxima_etapa("finalizacao")

elif st.session_state.etapa == "finalizacao":
    mensagem_final = """
    Documentos recebidos com sucesso! ✅

    O seu cadastro está a ser processado pela nossa equipa.
    Após enviar os documentos, daremos o próximo passo que será liberar o acesso ao treinamento ATENTIVA.
    Também iremos disponibilizar o acesso ao APP para início de atividades ok.

    Seja bem-vindo à Atentiva Transportes Executivos!
    
    Qualquer dúvida é só chamar.
    Abraços.
    """
    adicionar_mensagem("assistant", mensagem_final)
    
    if st.button("Iniciar Novo Cadastro"):
        st.session_state.clear()
        st.rerun()




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


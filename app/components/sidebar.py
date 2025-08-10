import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

def sidebar_area():
    VALID_FILES = ["PDF", "CSV", "URL"]

    MODEL_PARAMS = {
        'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o'], 'chat': ChatOpenAI},
        'Groq': {'modelos': ['llama-3.3-70b-versatile', 'gemma2-9b-it', 'qwen/qwen3-32b'], 'chat': ChatGroq}
    }

    tabs = st.tabs(["Upload"])

    with tabs[0]:
        file_type = st.selectbox("Tipo de arquivo", VALID_FILES)
        if file_type == "PDF":
            pdf_file = st.file_uploader("Carregue um arquivo PDF", type="pdf")
            if pdf_file:
                st.success("Arquivo carregado com sucesso ✅")
        elif file_type == "CSV":
            st.error(f"Carregamento de {file_type} ainda não implementado")
            # csv_file = st.file_uploader("Carregue um arquivo CSV", type="csv")
        else:
            st.error(f"Carregamento de {file_type} ainda não implementado")
            # url = st.text_input("Digite a URL do site")

        provider = st.selectbox("Tipo de modelo",
                                MODEL_PARAMS.keys())
        model = st.selectbox("Modelo",
                             MODEL_PARAMS[provider]['modelos'])
        api_key = st.text_input("Informe a chave de API",
                                type="password",
                                value=st.session_state.get(f'api_key_{provider}'))

        st.session_state[f'api_key_{provider}'] = api_key

    if st.button("Confirmar", use_container_width=True):
        if not api_key:
            st.error("Chave de API é obrigatória")
            st.stop()

        try:
            chat = MODEL_PARAMS[provider]['chat'](model=model, api_key=api_key)
            chat.invoke("Olá, IA!")

        except Exception as e:
            st.error("Chave inválida ou problemas de conexão com o modelo.")
            url = "https://platform.openai.com/account/api-keys"
            st.warning(f"Você pode verificar sua chave de API através da url: {url}")
            st.stop()

        st.session_state['chat'] = chat
        st.success("IA disponível para uso ✅")

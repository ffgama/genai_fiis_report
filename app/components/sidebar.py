import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from components.utils import load_pdf_document

def sidebar_area():
    EXT_TYPE_FILES = ["PDF", "CSV", "URL"]

    MODEL_PARAMS = {
        'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o'], 'chat': ChatOpenAI},
        'Groq': {'modelos': ['llama-3.3-70b-versatile', 'gemma2-9b-it', 'qwen/qwen3-32b'], 'chat': ChatGroq}
    }

    tabs = st.tabs(["🏠 Início", "⚠️ Disclaimer"])

    with tabs[0]:
        file_type = st.selectbox("Tipo de arquivo", EXT_TYPE_FILES)
        if file_type == "PDF":
            pdf_file = st.file_uploader("Carregue um arquivo PDF", type=['.pdf'])

            if pdf_file is not None:
                st.success("Arquivo carregado com sucesso ✅")
                document = load_pdf_document(pdf_file)
                st.session_state['document'] = document

        elif file_type == "CSV":
            st.error(f"Carregamento de {file_type} ainda não implementado")
        elif file_type == "URL":
            st.error(f"Carregamento de {file_type} ainda não implementado")

        provider = st.selectbox("Selecione o provedor",
                                MODEL_PARAMS.keys())
        model = st.selectbox("Selecione o modelo",
                             MODEL_PARAMS[provider]['modelos'])
        api_key = st.text_input("Informe a chave da API",
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

            except Exception:
                st.error("Chave inválida ou problemas de conexão com o modelo.")
                url = "https://platform.openai.com/account/api-keys"
                st.info(f"Você pode verificar sua chave de API através da url: {url}")
                st.stop()

            st.session_state['chat'] = chat
            st.success("IA disponível para uso ✅")

    with tabs[1]:
        st.warning(""" 👉 As informações fornecidas neste aplicativo são apenas
                   para fins educacionais e não representam recomendação
                   de investimento.""")
        st.warning(""" 👉 Uma inteligencia artificial pode gerar respostas
                   incorretas ou imprecisas. Sempre verifique as
                   informações obtidas com fontes confiáveis antes de tomar
                   decisões de investimento.""")

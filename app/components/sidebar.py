import streamlit as st


def sidebar_area():
    VALID_FILES = ["PDF", "CSV", "URL"]

    MODEL_CONFIG = {
        'Groq': {'modelos': ['deepseek-r1-distill-llama-70b','llama-3.1-70b-versatile', 'gemma2-9b-it', 'mixtral-8x7b-32768']},
        'OpenAI': {'modelos': ['gpt-4o-mini', 'gpt-4o']}
    }

    tabs = st.tabs(["Upload", "Modelo"])

    with tabs[0]:
        file_type = st.selectbox("Tipo de arquivo", VALID_FILES)
        if file_type == "PDF":
            pdf_file = st.file_uploader("Carregue um arquivo PDF", type="pdf")
        elif file_type == "CSV":
            csv_file = st.file_uploader("Carregue um arquivo CSV", type="csv")
        else:
            url = st.text_input("Digite a URL do site")

    with tabs[1]:
        provider = st.selectbox("Tipo de modelo",
                                MODEL_CONFIG.keys())
        model = st.selectbox("Modelo",
                             MODEL_CONFIG[provider]['modelos'])
        api_key = st.text_input("Informe a chave de API",
                                type="password",
                                value=st.session_state.get(f'api_key_{provider}'))

        st.session_state[f'api_key_{provider}'] = api_key
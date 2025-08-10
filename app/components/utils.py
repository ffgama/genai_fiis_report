import streamlit as st
import tempfile
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


@st.cache_data(show_spinner=False)
def load_pdf_document(pdf_file: str) -> list:

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
        temp.write(pdf_file.read())
        path = temp.name

    loader = PyPDFLoader(path)
    list_docs = loader.load()
    document = ["\n\n".join([doc.page_content for doc in list_docs])]
    return document


@st.cache_data(show_spinner=False)
def load_system_message(filepath: str) -> str:
    path = Path(filepath)
    if not path.is_file():
        st.error(f"Arquivo de prompt não encontrado: {filepath}")
        return ""
    return path.read_text(encoding="utf-8")

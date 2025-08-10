import tempfile
from langchain_community.document_loaders import PyPDFLoader


def load_pdf_document(pdf_file: str) -> None:

    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
        temp.write(pdf_file.read())
        path = temp.name

    loader = PyPDFLoader(path)
    list_docs = loader.load()
    document = ["\n\n".join([doc.page_content for doc in list_docs])]

    return document

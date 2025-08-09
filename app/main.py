import streamlit as st
from components.header import setup_page
from components.content import chat_area
from components.sidebar import sidebar_area


def main():
    setup_page()
    with st.sidebar:
        sidebar_area()
    chat_area()


if __name__ == "__main__":
    main()

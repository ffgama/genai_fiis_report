import streamlit as st
from components.content import chat_area
from components.sidebar import sidebar_area


def main():
    st.set_page_config(page_title="Bot do investidor", page_icon=":robot_face:")
    st.subheader("🤖 Acompanhe seus FIIs", divider=True)

    with st.sidebar:
        sidebar_area()

    if 'chat' in st.session_state:
        chat_area()


if __name__ == "__main__":
    main()

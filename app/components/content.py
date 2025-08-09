import streamlit as st


def chat_area():
    st.header("🤖 Acompanhe seus FIIs")

    messages = st.session_state.get("messages", [])
    for message in messages:
        chat = st.chat_message(message[0])
        chat.markdown(message[1])

    user_input = st.chat_input("Fale com o Oráculo dos Fundos imobiliários")
    if user_input:
        messages.append(('user', user_input))
        st.session_state['messages'] = messages
        st.rerun()

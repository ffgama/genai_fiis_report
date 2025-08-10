import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate


def execute_conversation_cycle(
        user_input: str,
        chat_model,
        chat_history,
        system_message: str,
        memory) -> None:

    # exibindo a mensagem do usuário na área do chat
    chat_human = st.chat_message('human')
    chat_human.markdown(user_input)

    # preparando o template do prompt
    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{user_input}')
    ])

    # criando uma chain
    chain = template | chat_model

    chat_ai = st.chat_message('ai')

    # streamando a conversa
    response = chat_ai.write_stream(
        chain.stream({
            'user_input': user_input,
            'chat_history': memory.buffer_as_messages
        })
    )

    # atualizando a memória do buffer com o histórico de conversa
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(response)
    st.session_state['memory'] = memory


def chat_area():
    # recuperando o modelo de chat da sessão do usuário
    chat_model = st.session_state.get('chat')
    # definindo a memória da conversa
    memory = st.session_state.get('memory', ConversationBufferMemory())
    # varrendo o buffer de memória para exibir as mensagens
    for msg in memory.chat_memory.messages:
        chat = st.chat_message(msg.type)
        chat.markdown(msg.content)

    user_input = st.chat_input("Fale com o Bot de Fundos imobiliários")

    if user_input:

        system_message = """
            Você é um assistente especializado em fundos imobiliários (FIIs)
            no Brasil.
            Seu objetivo é ajudar os usuários a entender e acompanhhar
            seus investimentos.
            Caso alguém pergunte sobre outro assunto, responda que
            você é especializado em FIIs e não pode ajudar com outros temas.
        """

        execute_conversation_cycle(
            user_input=user_input,
            chat_model=chat_model,
            chat_history=memory,
            system_message=system_message,
            memory=memory
        )

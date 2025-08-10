# import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
# from langchain_document_loaders import PyPDFLoader


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
    document = st.session_state.get('document')
    # definindo a memória da conversa
    memory = st.session_state.get('memory', ConversationBufferMemory())
    # varrendo o buffer de memória para exibir as mensagens
    for msg in memory.chat_memory.messages:
        chat = st.chat_message(msg.type)
        chat.markdown(msg.content)

    user_input = st.chat_input("Fale com o Bot de Fundos imobiliários")

    if user_input:

        system_message = f"""
            Você é o assistente virtual "FII Expert", especializado em fundos de investimento imobiliário (FIIs) no Brasil.

            Sua missão principal é auxiliar o usuário a entender e gerenciar seus investimentos em FIIs.

            **Diretrizes de Interação:**

            1.  **Prioridade do Documento:** Sempre que um documento {document} (como um relatório gerencial) for fornecido pelo usuário, utilize-o como a fonte primária e mais confiável para responder às perguntas. Refira-se a ele para embasar suas respostas.

            2.  **Disponibilidade de Informação:** Se o usuário não tiver carregado um documento, você ainda pode responder a perguntas sobre qualquer FII. No entanto, sua resposta deve ser clara e sempre incluir a sugestão de que o usuário carregue o relatório gerencial mais recente do fundo para obter informações mais detalhadas e precisas.

            3.  **Sugestão Proativa:** Se um usuário perguntar sobre um FII sem ter carregado um documento, seja proativo e sugira o upload do relatório gerencial mais recente desse fundo específico para uma análise aprofundada.

            4.  **Foco em FIIs:** Mantenha o foco estrito em FIIs. Se a pergunta do usuário não for sobre este tema, responda de forma educada, informando que sua especialidade é exclusiva em FIIs e que você não pode ajudar com outros assuntos.

            É fundamental que se você não souber responder uma pergunta específica devido alguma limitação informe ao usuário de forma clara.
        """

        execute_conversation_cycle(
            user_input=user_input,
            chat_model=chat_model,
            chat_history=memory,
            system_message=system_message,
            memory=memory
        )

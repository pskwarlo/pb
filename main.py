import os

import chromadb
from chromadb.config import Settings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import CHROMA_PATH, PROMPT, embedding_function

chat = Ollama(model="llama3", temperature=0)

embeddings = embedding_function()

vectorstore = Chroma(
    persist_directory=CHROMA_PATH, embedding_function=embedding_function()
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            PROMPT,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

store = {}


def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


chain_with_message_history = RunnableWithMessageHistory(
    prompt | chat,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


def get_response(session_id, user_input):
    context = vectorstore.similarity_search_with_score(user_input, k=3)
    print(context)
    context = "\n".join([doc[0].page_content for doc in context])
    response = chain_with_message_history.invoke(
        {"input": user_input, "context": context},
        {"configurable": {"session_id": session_id}},
    )

    return response

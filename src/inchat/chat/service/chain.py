from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain import hub
from langchain.chat_models import ChatOllama
from langchain.vectorstores.pgvector import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.config import vector_connection_string, settings


model = settings.ollama_model
ollama_url = settings.ollama_url

llm = Ollama(base_url = ollama_url, model = model, temperature=0.3, top_p = 0.9, top_k = 40)
chat = ChatOllama(base_url = ollama_url, model = model, temperature=0.3, top_p = 0.9, top_k = 40)
embeddings = OllamaEmbeddings(base_url = ollama_url, model = model)
output_parser = StrOutputParser()
prompt = hub.pull("rlm/rag-prompt")

contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
contextualize_q_chain = contextualize_q_prompt | llm | output_parser

qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
def contextualized_question(data: dict):
    return contextualize_q_chain if data.get("chat_history") else data["question"]

def get_chain_with_retriever(retriever_collection_name):
    store = PGVector(
        collection_name=retriever_collection_name,
        connection_string=vector_connection_string,
        embedding_function=embeddings,
    )
    retriever = store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    rag_chain = (RunnablePassthrough.assign(context=contextualized_question | retriever) | qa_prompt | llm)  # noqa
    return rag_chain
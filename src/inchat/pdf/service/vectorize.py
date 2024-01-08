from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.config import vector_connection_string, settings


model = settings.ollama_model
embeddings = OllamaEmbeddings(base_url = settings.ollama_url, model = model )

async def vectorize(collection_name: str, text: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    texts = text_splitter.split_text(text)
    await PGVector.afrom_texts(embedding=embeddings,
                               texts=texts,
                               collection_name=collection_name,
                               connection_string=vector_connection_string)

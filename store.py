from functools import lru_cache

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import config

@lru_cache(maxsize=1)
def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    config.require_api_key()
    return GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(config.VECTORSTORE_DIR),
    )
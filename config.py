import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
COLLECTION_NAME = "novatech_handbook"

# Modelos (el MISMO modelo de embeddings se usa para indexar y para consultar)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.8-flash")

# Chunking, medido en TOKENS (tiktoken cl100k_base)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Recuperación: entre 3 y 5 para evitar "Lost in the Middle"
TOP_K = 4


def require_api_key() -> None:
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "Falta GOOGLE_API_KEY. Copiá .env.example a .env y completá tu clave."
        )

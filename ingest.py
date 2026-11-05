from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config
from store import get_vectorstore

SUPPORTED_EXTENSIONS = {".txt", ".md"}
MANIFEST_PATH = config.VECTORSTORE_DIR / "manifest.json"


def _data_files(data_dir: Path) -> list[Path]:
    return sorted(
        p for p in data_dir.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def load_documents(data_dir: Path = config.DATA_DIR) -> list[Document]:
    """Lee todos los .txt/.md de la carpeta data/."""
    docs = [
        Document(
            page_content=path.read_text(encoding="utf-8"),
            metadata={"source": path.name},
        )
        for path in _data_files(data_dir)
    ]
    if not docs:
        raise FileNotFoundError(f"No hay archivos .txt/.md en {data_dir}")
    return docs


def split_documents(docs: list[Document]) -> list[Document]:
    """Chunking con RecursiveCharacterTextSplitter medido en tokens.

    Los separadores priorizan cortar en títulos de Markdown y luego en
    párrafos, para que cada chunk conserve sentido semántico."""
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n# ", "\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    counters: dict[str, int] = defaultdict(int)
    for chunk in chunks:
        source = chunk.metadata["source"]
        idx = counters[source]
        counters[source] += 1
        chunk.metadata["chunk_index"] = idx
        chunk.metadata["chunk_id"] = f"{source}#{idx}"  # ID estable y citable
    return chunks


def compute_fingerprint(data_dir: Path = config.DATA_DIR) -> str:
    """Hash de contenido + configuración. Si cambia algo, hay que reindexar."""
    h = hashlib.sha256()
    for path in _data_files(data_dir):
        h.update(path.name.encode())
        h.update(path.read_bytes())
    h.update(
        f"{config.EMBEDDING_MODEL}|{config.CHUNK_SIZE}|{config.CHUNK_OVERLAP}".encode()
    )
    return h.hexdigest()


def _read_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def _write_manifest(fingerprint: str, n_chunks: int) -> None:
    config.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(
            {
                "fingerprint": fingerprint,
                "n_chunks": n_chunks,
                "embedding_model": config.EMBEDDING_MODEL,
                "chunk_size": config.CHUNK_SIZE,
                "chunk_overlap": config.CHUNK_OVERLAP,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def ingest(force: bool = False) -> Chroma:
    vectorstore = get_vectorstore()
    fingerprint = compute_fingerprint()
    existing = vectorstore._collection.count()  # nº de chunks ya persistidos

    up_to_date = _read_manifest().get("fingerprint") == fingerprint
    if existing > 0 and up_to_date and not force:
        print(f"[ingesta] Base existente ({existing} chunks). No se reindexa.")
        return vectorstore

    if existing > 0:
        print("[ingesta] Cambios detectados (o --force): reconstruyendo colección...")
        vectorstore.reset_collection()

    docs = load_documents()
    chunks = split_documents(docs)
    vectorstore.add_documents(chunks, ids=[c.metadata["chunk_id"] for c in chunks])
    _write_manifest(fingerprint, len(chunks))
    print(f"[ingesta] {len(docs)} documentos -> {len(chunks)} chunks indexados.")
    return vectorstore


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingesta de documentos a ChromaDB")
    parser.add_argument("--force", action="store_true", help="reindexar desde cero")
    ingest(force=parser.parse_args().force)

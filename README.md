# RAG local con ChromaDB + LangChain (LCEL) + Gemini — Pre-entrega 3

Sistema de recuperación semántica local (RAG) de punta a punta: ingesta de documentos
→ base vectorial persistente (ChromaDB) → recuperación top-k → generación *grounded*
con LCEL, asíncrona y con salida estructurada (Pydantic).

El dataset de ejemplo es un handbook **ficticio** de una empresa (NovaTech S.A.), a
propósito: así se puede comprobar que el modelo responde desde los documentos y no
desde su conocimiento previo.

## Estructura

```
.
├── data/                      # Dataset de ejemplo (4 archivos .md)
├── config.py                  # Parámetros compartidos (chunking, top_k, modelos)
├── store.py                   # Embeddings + cliente persistente de Chroma (único punto)
├── ingest.py                  # Ingesta: carga -> chunking -> ChromaDB (idempotente)
├── rag.py                     # Cadena LCEL asíncrona + get_rag_response()
├── run_tests.py               # Pruebas: pregunta con respuesta y preguntas trampa
├── requirements.txt
├── .env.example               # Plantilla de variables de entorno (sin claves reales)
└── .gitignore                 # Excluye .env y vectorstore/
```

## Cómo ejecutarlo

1. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar la clave de API:
   ```bash
   cp .env.example .env             # Windows: copy .env.example .env
   # editar .env y completar GOOGLE_API_KEY
   ```
4. Indexar los documentos (opcional: `rag.py` lo hace solo si la base no existe):
   ```bash
   python ingest.py
   ```
5. Hacer una consulta o correr las pruebas:
   ```bash
   python rag.py "¿Cuántos días de vacaciones me corresponden con 5 años?"
   python run_tests.py
   ```

Uso desde código:

```python
import asyncio
from rag import get_rag_response

resp = asyncio.run(get_rag_response("¿Cuál es el límite de alojamiento en el exterior?"))
print(resp.answer, resp.references)
```

## Decisiones de diseño

| Requisito | Cómo se resuelve |
|---|---|
| Chunking ≥ 500 tokens, overlap 50 | `RecursiveCharacterTextSplitter.from_tiktoken_encoder` con `chunk_size=500`, `chunk_overlap=50` (tokens reales, no caracteres). Separadores que priorizan títulos y párrafos de Markdown. |
| ChromaDB local persistente | `Chroma(persist_directory="./vectorstore")` en `store.py`. |
| Mismos embeddings al indexar y consultar | `ingest.py` y `rag.py` obtienen los embeddings de `store.get_embeddings()`. No existe otro camino. |
| Persistencia / no reindexar | `ingest()` compara una huella (hash de documentos + modelo de embeddings + parámetros de chunking) guardada en `vectorstore/manifest.json`. Si coincide, no reindexa; si algo cambió, reconstruye la colección. |
| `top_k` 3–5 | `TOP_K = 4` en `config.py`. |
| Prompt "filtro de veracidad" | Prompt de sistema en `rag.py`: responde solo con el CONTEXTO y, si no está, devuelve exactamente "No lo sé…". |
| Cadena LCEL | `RunnableParallel(docs=retriever, question=...) \| assign(context) \| prompt \| llm \| PydanticOutputParser`. |
| Asíncrono | `get_rag_response()` es `async` y usa `chain.ainvoke()`. |
| Salida Pydantic | `RAGResponse(answer, has_answer, references)`. Las referencias se filtran para que solo queden IDs de chunks realmente recuperados (anti-alucinación de citas). |
| Sin llaves en el repo | `GOOGLE_API_KEY` se lee de `.env` (ignorado por git). Solo se versiona `.env.example`. |

## Pruebas

`python run_tests.py` ejecuta:

1. **Pregunta con respuesta**: *"Tengo 5 años de antigüedad, ¿cuántos días hábiles de vacaciones me corresponden?"* → debe responder 20 días y citar `01_vacaciones_y_licencias.md#N`.
2. **Pregunta trampa**: *"¿Cuál es el sueldo del gerente general de NovaTech?"* → no está en los documentos; debe responder "No lo sé…", `has_answer=false`, sin referencias.
3. **Trampa extra** (fuera de dominio): *"¿Cuál es la capital de Francia?"* → mismo comportamiento.

El script termina con código 0 si todas pasan y 1 si alguna falla.

## Cambiar de proveedor

Solo hay que modificar `store.get_embeddings()` y el `ChatGoogleGenerativeAI` de `rag.build_chain()` (por ejemplo, a `OpenAIEmbeddings` y `ChatOpenAI`).
Si cambiás el modelo de embeddings, la huella cambia y la base se reconstruye sola.

## Seguridad

Nunca subas tu `.env`. Si una clave se filtra por error, revocala de inmediato.

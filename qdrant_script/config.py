from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Embedding model
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"

model = SentenceTransformer(EMBEDDING_MODEL)

client = QdrantClient(
    host="localhost",
    port=6333
)

EMBEDDING_DIM = model.get_embedding_dimension()
# import json
# from pathlib import Path

# from ollama import Client
# from qdrant_client import QdrantClient
# from qdrant_client.models import (
#     Distance,
#     PointStruct,
#     VectorParams,
# )

# # --------------------------------------------------
# # CONFIGURATION
# # --------------------------------------------------

# OLLAMA_URL = "http://localhost:11434"
# EMBEDDING_MODEL = "nomic-embed-text"

# QDRANT_HOST = "localhost"
# QDRANT_PORT = 6333



# BASE_DIR = Path(__file__).resolve().parent.parent

# # Always change data here before uploading
# LAW_NAME = "THE SEXUAL HARASSMENT OF WOMEN AT WORKPLACE (PREVENTION, PROHIBITION AND REDRESSAL) ACT, 2013"
# LAW_CODE = "POSH"
# LAW_YEAR = 2021
# DATA_FOLDER = BASE_DIR / "Raw_Law_Extractors" / "posh" # Change to insert new data
# CHUNKS_FILE= BASE_DIR / "Raw_Law_Extractors" / "posh" / "posh_chunks.json"
# SECTIONS_FILE= BASE_DIR / "Raw_Law_Extractors" / "posh" / "posh_sections.json"
# DEFINITIONS_FILE= BASE_DIR / "Raw_Law_Extractors" / "posh" / "posh_definitions.json"
# # --------------------------------------------------
# # CONNECT
# # --------------------------------------------------

# ollama = Client(host=OLLAMA_URL)

# qdrant = QdrantClient(
#     host=QDRANT_HOST,
#     port=QDRANT_PORT
# )

# # --------------------------------------------------
# # EMBEDDING FUNCTION
# # --------------------------------------------------

# def embed(text: str):

#     response = ollama.embed(
#         model=EMBEDDING_MODEL,
#         input=text
#     )

#     return response["embeddings"][0]

# # --------------------------------------------------
# # GET EMBEDDING DIMENSION
# # --------------------------------------------------

# sample_vector = embed("Hello World")

# VECTOR_SIZE = len(sample_vector)

# print(f"Embedding Dimension: {VECTOR_SIZE}")

# # --------------------------------------------------
# # CREATE COLLECTION
# # --------------------------------------------------

# def create_collection(name):

#     collections = qdrant.get_collections().collections

#     existing = [c.name for c in collections]

#     if name in existing:
#         print(f"{name} already exists.")
#         return

#     qdrant.create_collection(
#         collection_name=name,
#         vectors_config=VectorParams(
#             size=VECTOR_SIZE,
#             distance=Distance.COSINE
#         )
#     )

#     print(f"Created collection: {name}")

# # --------------------------------------------------
# # GENERIC UPLOAD FUNCTION
# # --------------------------------------------------

# def upload_json(
#     json_file,
#     collection_name,
#     text_builder
# ):

#     create_collection(collection_name)

#     with open(json_file, "r", encoding="utf8") as f:
#         documents = json.load(f)

#     points = []

#     for idx, document in enumerate(documents):

#         text = text_builder(document)

#         vector = embed(text)

#         payload = {
#             **document,
#             "law": LAW_NAME,
#             "law_code": LAW_CODE,
#             "year": LAW_YEAR
#         }

#         points.append(
#         PointStruct(
#             id=idx,
#             vector=vector,
#             payload=payload
#         )
#     )

#     qdrant.upsert(
#         collection_name=collection_name,
#         points=points
#     )

#     print(f"Uploaded {len(points)} records -> {collection_name}")

# # --------------------------------------------------
# # DEFINITIONS
# # --------------------------------------------------

# upload_json(

#     json_file=DATA_FOLDER / DEFINITIONS_FILE,

#     collection_name="definitions",

#     text_builder=lambda x: f"""
# Definition

# Term:
# {x["term"]}

# Meaning:
# {x["definition"]}
# """

# )

# # --------------------------------------------------
# # SECTIONS
# # --------------------------------------------------

# upload_json(

#     json_file=DATA_FOLDER / SECTIONS_FILE,

#     collection_name="sections",

#     text_builder=lambda x: f"""
# Section {x["section"]}

# Title:
# {x["heading"]}

# {x["text"]}
# """

# )

# # --------------------------------------------------
# # CHUNKS
# # --------------------------------------------------

# upload_json(

#     json_file=DATA_FOLDER / CHUNKS_FILE,

#     collection_name="chunks",

#     text_builder=lambda x: f"""
# Section {x["section"]}

# Subsection:
# {x.get("subsection", "")}

# Title:
# {x["heading"]}

# {x["chunk"]}
# """

# )

# print("\nAll documents uploaded successfully!")



# # ingest testing

# from ollama import Client
# from qdrant_client import QdrantClient

# ollama = Client(host="http://localhost:11434")

# client = QdrantClient(
#     host="localhost",
#     port=6333
# )

# query = "What is the POSH ACT"

# embedding = ollama.embed(
#     model="nomic-embed-text",
#     input=query
# )["embeddings"][0]

# results = client.query_points(
#     collection_name="definitions",
#     query=embedding,
#     limit=5
# )

# for point in results.points:

#     print("=" * 60)
#     print("Score:", point.score)
#     print(point.payload)
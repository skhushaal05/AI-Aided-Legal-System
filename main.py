from ollama import Client
from qdrant_client import QdrantClient

ollama = Client(host="http://localhost:11434")


qdrant = QdrantClient(
    host="localhost",
    port=6333
)

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3:8b"
q="""The Situation:
Anita is a senior marketing executive at a mid-sized corporate firm. Over the past three months, her reporting manager, Rohan, has been making frequent, uninvited comments about her physical appearance. He often texts her late at night asking her out for drinks, which she has repeatedly and politely declined.

Recently, during a performance appraisal discussion, Rohan implied that Anita’s upcoming promotion to Team Lead would be "guaranteed" if she agreed to accompany him on a personal weekend trip. When Anita flatly refused, Rohan's behavior escalated. He began leaving her off critical calendar invites, publicly humiliating her over minor errors, and ultimately gave her a poor performance rating, citing "lack of team cooperation."

The Question
Based on the scenario above: What specific types of sexual harassment has Anita faced, and what key sections of the POSH Act, 2013 apply to her situation regarding the offense, how she should report it, and the employer's responsibilities?
"""

def ask(question):

    embedding = ollama.embed(
        model=EMBED_MODEL,
        input=question
    )["embeddings"][0]

    results = qdrant.query_points(
        collection_name="chunks",
        query=embedding,
        limit=5
    )

    context = ""

    for point in results.points:

        payload = point.payload

        context += f"""
Section {payload['section']}

Heading:
{payload['heading']}

{payload['chunk']}

------------------------
"""

    prompt = f"""
You are a POSH Act legal assistant working with internal complaints committee.
Answer ONLY from the supplied context.

Context:

{context}

Question:

{question}

Answer:
"""

    answer = ollama.chat(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "assistant",
                "content": prompt
            }
        ]
    )

    print(answer["message"]["content"])

ask(q)

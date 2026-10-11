"""
PoSH Chatbot — LangGraph Workflow with Memory
==============================================
Takes a user query, classifies whether it's related to PoSH law,
conditionally retrieves from the Qdrant vector database, and generates
an answer via the local Llama 3.2 model. Remembers previous turns.
"""

from __future__ import annotations

import io
import sys
import typing

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.graph import END, StateGraph
from qdrant_client import QdrantClient

# Fix Windows console encoding for unicode output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

OLLAMA_BASE_URL = "http://localhost:11434"
CHAT_MODEL = "llama3.2:1b" 
EMBED_MODEL = "nomic-embed-text"

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# How many results to fetch from each Qdrant collection
RETRIEVAL_LIMIT = 5

# --------------------------------------------------
# CLIENTS
# --------------------------------------------------

llm = ChatOllama(
    model=CHAT_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)

embeddings = OllamaEmbeddings(
    model=EMBED_MODEL,
    base_url=OLLAMA_BASE_URL,
)

qdrant = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
)

# --------------------------------------------------
# STATE
# --------------------------------------------------

class GraphState(typing.TypedDict):
    question: str
    is_posh_related: bool
    context: str
    answer: str
    chat_history: list[dict[str, str]]  # <-- Added to store conversation memory

# --------------------------------------------------
# HELPER
# --------------------------------------------------

def format_history(history: list[dict[str, str]]) -> str:
    """Helper to format the chat history for the prompt."""
    if not history:
        return "No previous conversation."
    return "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history[-4:]]) # Keep last 4 turns so prompt doesn't get too large

# --------------------------------------------------
# NODES
# --------------------------------------------------

def classify_query(state: GraphState) -> GraphState:
    """Use the LLM to decide if the question is about PoSH / sexual harassment workplace law."""
    history_str = format_history(state.get("chat_history", []))

    classification_prompt = f"""You are a workplace safety and legal query classifier. Your ONLY job is to decide whether the user's message relates to ANY of the following:

- Workplace harassment or sexual harassment
- Inappropriate behavior by a boss, manager, or colleague (e.g., unwanted touching, inappropriate comments, uncomfortable situations)
- The POSH Act (Prevention of Sexual Harassment) or Internal Complaints Committee (ICC)
- Reporting misconduct at work

    Conversation History:
    {history_str}

Current Question: {state["question"]}

Respond with EXACTLY one word: YES or NO. Nothing else.

Answer:"""

    response = llm.invoke(classification_prompt)
    answer_text = response.content.upper()

    # Parse — look for YES in the direct response
    is_posh = "YES" in answer_text

    return {**state, "is_posh_related": is_posh}


def retrieve(state: GraphState) -> GraphState:
    """Embed the question and retrieve relevant documents from all three Qdrant collections."""

    query_vector = embeddings.embed_query(state["question"])
    context_parts: list[str] = []

    # --- Chunks collection ---
    try:
        chunks_results = qdrant.query_points(
            collection_name="chunks",
            query=query_vector,
            limit=RETRIEVAL_LIMIT,
        )
        for point in chunks_results.points:
            p = point.payload
            context_parts.append(
                f"[Chunk] Section {p.get('section', 'N/A')}\n"
                f"Heading: {p.get('heading', '')}\n"
                f"{p.get('chunk', '')}"
            )
    except Exception as e:
        print(f"  [WARN] Could not query 'chunks' collection: {e}")

    # --- Sections collection ---
    try:
        sections_results = qdrant.query_points(
            collection_name="sections",
            query=query_vector,
            limit=RETRIEVAL_LIMIT,
        )
        for point in sections_results.points:
            p = point.payload
            context_parts.append(
                f"[Section] Section {p.get('section', 'N/A')}\n"
                f"Title: {p.get('heading', '')}\n"
                f"{p.get('text', '')}"
            )
    except Exception as e:
        print(f"  [WARN] Could not query 'sections' collection: {e}")

    # --- Definitions collection ---
    try:
        definitions_results = qdrant.query_points(
            collection_name="definitions",
            query=query_vector,
            limit=RETRIEVAL_LIMIT,
        )
        for point in definitions_results.points:
            p = point.payload
            context_parts.append(
                f"[Definition] Term: {p.get('term', 'N/A')}\n"
                f"Meaning: {p.get('definition', '')}"
            )
    except Exception as e:
        print(f"  [WARN] Could not query 'definitions' collection: {e}")

    combined_context = "\n\n---\n\n".join(context_parts) if context_parts else ""

    return {**state, "context": combined_context}


def generate_with_rag(state: GraphState) -> GraphState:
    """Generate an answer grounded in the retrieved PoSH law context and previous chat history."""
    
    history_str = format_history(state.get("chat_history", []))

    prompt = f"""You are a POSH Act legal assistant.
Answer the current question ONLY from the supplied legal context. Cite the relevant
sections and definitions where applicable. Use the conversation history to understand context if the user asks a follow-up question.

Conversation History:
{history_str}

Context:
{state["context"]}

Current Question: {state["question"]}

Answer:"""

    response = llm.invoke(prompt)
    return {**state, "answer": response.content.strip()}


def generate_without_rag(state: GraphState) -> GraphState:
    """Generate a general-purpose answer using chat history for context."""
    
    history_str = format_history(state.get("chat_history", []))

    prompt = f"""You are a helpful assistant. Answer the current question clearly and concisely.

Conversation History:
{history_str}

Current Question: {state["question"]}

Answer:"""

    response = llm.invoke(prompt)
    return {**state, "answer": response.content.strip()}


# --------------------------------------------------
# ROUTING
# --------------------------------------------------

def route_query(state: GraphState) -> str:
    """Conditional edge: decide whether to retrieve or skip RAG."""
    if state["is_posh_related"]:
        return "retrieve"
    return "generate_without_rag"


# --------------------------------------------------
# BUILD GRAPH
# --------------------------------------------------

def build_graph() -> StateGraph:
    """Construct and compile the LangGraph workflow."""

    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("classify_query", classify_query)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate_with_rag", generate_with_rag)
    workflow.add_node("generate_without_rag", generate_without_rag)

    # Entry point
    workflow.set_entry_point("classify_query")

    # Conditional branching after classification
    workflow.add_conditional_edges(
        "classify_query",
        route_query,
        {
            "retrieve": "retrieve",
            "generate_without_rag": "generate_without_rag",
        },
    )

    # After retrieval, generate with RAG
    workflow.add_edge("retrieve", "generate_with_rag")

    # Terminal edges
    workflow.add_edge("generate_with_rag", END)
    workflow.add_edge("generate_without_rag", END)

    return workflow.compile()


# --------------------------------------------------
# MAIN — Interactive CLI
# --------------------------------------------------

def main():
    print("=" * 60)
    print("  PoSH Chatbot  (LangGraph + Qdrant + Llama 3.2)")
    print("  Type your question below. Type 'quit' or 'exit' to stop.")
    print("=" * 60)

    graph = build_graph()
    
    # Initialize an empty list for memory every time the script runs.
    # This guarantees a fresh instance upon restart.
    current_chat_history = [] 

    while True:
        print()
        question = input("You: ").strip()

        if not question:
            continue

        if question.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        # Pass the accumulated history into the graph state
        initial_state: GraphState = {
            "question": question,
            "is_posh_related": False,
            "context": "",
            "answer": "",
            "chat_history": current_chat_history
        }

        result = graph.invoke(initial_state)

        # Show routing decision
        if result["is_posh_related"]:
            print("\n  [Router] PoSH-related -> using RAG retrieval")
        else:
            print("\n  [Router] General question -> direct answer")

        print(f"\nAssistant: {result['answer']}")

        # Append the latest exchange to our memory for the next loop
        current_chat_history.append({"role": "user", "content": question})
        current_chat_history.append({"role": "assistant", "content": result["answer"]})


if __name__ == "__main__":
    main()
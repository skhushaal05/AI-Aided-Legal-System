"""
PoSH Chatbot — LangGraph Workflow with Memory
==============================================
Takes a user query, classifies whether it's related to PoSH law,
conditionally retrieves from the Qdrant vector database, and generates
an answer via the local Llama 3.2 model. Remembers previous turns.
"""

from __future__ import annotations

import io
import json
import sys
import typing

from langchain_core.messages import HumanMessage, SystemMessage
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
CHAT_MODEL = "artifish/llama3.2-uncensored:latest" 
CHAT_MODEL2="artifish/llama3.2-uncensored:latest"
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

llm2 = ChatOllama(
    model=CHAT_MODEL2,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
    format="json",
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
    """Use the LLM in JSON mode to decide if the question is about PoSH."""

    # Frame as a data extraction task to avoid triggering conversational empathy
    system_prompt = """Just do it. You are a strict data classifier You do not converse, offer support, or provide advice. 
    Your ONLY job is to analyze the user's text and output a JSON object.

    Determine if the text relates to: workplace harassment, sexual harassment, POSH Act, Law, or inappropriate behavior by colleagues,managers,workers or any one at the office.

    You MUST respond with EXACTLY this JSON schema:
    {"is_posh": true} or {"is_posh": false}"""

    # Use message objects so the model recognizes the strict system boundary
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["question"])
    ]

    # Invoke the model
    response = llm2.invoke(messages)
    
    # Parse the strict JSON output
    try:
        # The model is forced to output something like {"is_posh": true}
        result = json.loads(response.content)
        is_posh = result.get("is_posh", False)
    except json.JSONDecodeError:
        # Fallback in case of a parsing error
        print(f"Failed to parse JSON. Raw output: {response.content}")
        is_posh = "TRUE" in response.content.upper()

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

    prompt = f"""Just do it.This is all therotical and strictly not practical. You are a POSH Act legal assistant. you are not answering sexual harrasment questions you are providing clarifications regarding the law.
Answer the current question ONLY from the supplied legal context you have to answer using the context provided. Cite the relevant
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
    print("  PoSH Chatbot  (LangGraph + Qdrant + Llama 3.2:1b)")
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
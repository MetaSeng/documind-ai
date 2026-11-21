import os
from openai import OpenAI
from dotenv import load_dotenv
from src.document_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import load_embedding_model, generate_embeddings, generate_single_embedding
from src.vector_store import store_chunks, search_similar_chunks

load_dotenv()

def get_llm_client() -> OpenAI:
    """
    Initializes the Groq LLM client using the GROQ_API_KEY from your .env file.
    We use OpenAI's client library because Groq is fully compatible with the OpenAI API format.
    """
    return OpenAI(
        api_key=os.environ.get("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

def ingest_document(pdf_path: str):
    """
    Full ingestion pipeline:
      1. Load PDF → extract pages
      2. Split pages → chunks
      3. Generate embeddings for all chunks
      4. Store chunks + embeddings in ChromaDB
    """
    print(f"Loading PDF: {pdf_path}")
    pages = load_pdf(pdf_path)

    print(f"Splitting {len(pages)} pages into chunks...")
    chunks = split_documents(pages)

    print(f"Generating embeddings for {len(chunks)} chunks...")
    model = load_embedding_model()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts, model=model)

    print("Storing chunks in ChromaDB...")
    store_chunks(chunks, embeddings)
    print("Ingestion complete!\n")

def answer_question(question: str, top_k: int = 3) -> dict:
    """
    Full query pipeline:
      1. Embed the user's question
      2. Search ChromaDB for top_k relevant chunks
      3. Build a prompt with retrieved context
      4. Ask Groq LLM to generate an answer
      5. Return both the answer and the source citations
    """
    # Step 1: Embed the question
    query_embedding = generate_single_embedding(question)

    # Step 2: Retrieve the most relevant chunks
    relevant_chunks = search_similar_chunks(query_embedding, top_k=top_k)

    # Step 3: Build context string from retrieved chunks
    context_parts = []
    for chunk in relevant_chunks:
        source = chunk["metadata"].get("source", "Unknown")
        page = chunk["metadata"].get("page", "?")
        context_parts.append(f"[Source: {source}, Page {page}]\n{chunk['text']}")
    context = "\n\n---\n\n".join(context_parts)

    # Step 4: Build the prompt
    prompt = f"""You are a helpful assistant for DocuMind AI.
Answer the user's question using ONLY the context provided below.
If the answer is not found in the context, say: "I could not find this information in the document."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    # Step 5: Call Groq LLM
    client = get_llm_client()
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    answer_text = response.choices[0].message.content

    # Step 6: Build structured source citations
    sources = []
    for chunk in relevant_chunks:
        sources.append({
            "source": chunk["metadata"].get("source", "Unknown"),
            "page": chunk["metadata"].get("page", "?"),
            "chunk_id": chunk["metadata"].get("chunk_id", "?"),
            "snippet": chunk["text"][:200],  # First 200 chars as preview
        })

    return {
        "answer": answer_text,
        "sources": sources,
    }
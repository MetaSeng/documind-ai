import chromadb
from chromadb.config import Settings

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "documind"

def get_chroma_client() -> chromadb.PersistentClient:
    """
    Creates (or reconnects to) a persistent ChromaDB database saved
    in the local 'chroma_db/' folder.
    """
    return chromadb.PersistentClient(path=CHROMA_PATH)

def get_or_create_collection(client: chromadb.PersistentClient):
    """
    Gets an existing ChromaDB collection or creates a new one.
    A 'collection' is like a table in a traditional database.
    """
    return client.get_or_create_collection(name=COLLECTION_NAME)

def store_chunks(chunks: list[dict], embeddings: list[list[float]]):
    """
    Saves all text chunks and their embedding vectors into ChromaDB.
    Each chunk is stored with:
      - A unique ID
      - Its embedding vector
      - The raw text (called 'document' in ChromaDB)
      - The metadata (source file, page number, chunk_id)
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    ids = [str(chunk["metadata"]["chunk_id"]) for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )
    print(f"Stored {len(chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}'.")

def search_similar_chunks(query_embedding: list[float], top_k: int = 3) -> list[dict]:
    """
    Takes a query embedding (from a user's question) and returns
    the top_k most semantically similar chunks from ChromaDB.
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    # Reshape ChromaDB's nested results into a clean list of dicts
    chunks = []
    for text, metadata in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({
            "text": text,
            "metadata": metadata,
        })
    return chunks
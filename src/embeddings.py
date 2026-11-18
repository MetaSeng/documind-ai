from sentence_transformers import SentenceTransformer

DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"

def load_embedding_model(model_name: str = DEFAULT_MODEL_NAME) -> SentenceTransformer:
    """
    Loads the sentence-transformer model onto your local machine.
    Downloads the model weights once and caches them locally.
    """
    return SentenceTransformer(model_name)

def generate_embeddings(texts: list[str], model: SentenceTransformer = None) -> list[list[float]]:
    """
    Takes a list of text strings and converts each into a 384-dimensional vector.
    Returns a list of vectors (each vector is a list of floats).
    """
    if model is None:
        model = load_embedding_model()
    
    # model.encode converts text to NumPy arrays
    embeddings = model.encode(texts, show_progress_bar=False)
    
    # Convert NumPy arrays to standard Python lists for easy storage
    return embeddings.tolist()

def generate_single_embedding(text: str, model: SentenceTransformer = None) -> list[float]:
    """
    Converts a single string (like a user question) into an embedding vector.
    """
    if model is None:
        model = load_embedding_model()
        
    embedding = model.encode(text)
    return embedding.tolist()
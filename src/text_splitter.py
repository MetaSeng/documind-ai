def split_documents(
    documents: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list[dict]:
    """ Takes a list of document pages from document_loader.py, splits each page's text into smaller overlapping chunks, and preserves the source and page metadata.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be strictly smaller than chunk_size")

    chunks = []
    chunk_counter = 0

    for doc in documents:
        text = doc.get("text", "")
        base_metadata = doc.get("metadata", {})

        start = 0
        step = chunk_size - chunk_overlap # How far forward we jump for the next chunk


        while start < len(text):
            chunk_text = text[start : start + chunk_size].strip()

            if chunk_text:
                chunk_counter += 1
            
                # Copy existing metadata (source, page) and add chunk id
                chunk_metadata = base_metadata.copy()
                chunk_metadata["chunk_id"] = chunk_counter 

                chunks.append({
                    "text" : chunk_text,
                    "metadata" : chunk_metadata,
                })

            start += step
    return chunks
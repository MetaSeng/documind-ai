from pathlib import Path
import pypdf

def load_pdf(file_path: str) -> list[dict]:
    pages = []
    with open(file_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page_num, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append({
                    "text": text,
                    "metadata": {
                        "source": Path(file_path).name,
                        "page": page_num,
                    },
                })
    return pages

if __name__ == "__main__":
    result = load_pdf("data/Cambodia Trending Cars Report 2026 (1).pdf")
    print(f"Loaded {len(result)} pages.")
    print(result[0]["metadata"])
    print(result[0]["text"][:500])  # print first 500 characters of page 1
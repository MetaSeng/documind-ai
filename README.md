# 🧠 DocuMind AI

An intelligent, lightweight **Retrieval-Augmented Generation (RAG)** application built in vanilla Python. DocuMind AI allows users to ingest complex PDF documents, index their contents using local vector embeddings, and ask natural language questions with answers strictly grounded in the document context.

---

## 🌟 Key Highlights

- **Built from First Principles**: Implemented in clean, modular, vanilla Python without heavy orchestration frameworks (no LangChain or LangGraph), ensuring full control, faster startup times, and minimal abstraction overhead.
- **Privacy & Cost-Efficient**: Uses local sentence-transformer models (`all-MiniLM-L6-v2`) running directly on Apple Silicon / CPU for zero API cost during vector embedding.
- **Fast Inference via Groq**: Integrated with Groq's low-latency API (`qwen/qwen3.8-27b`) for ultra-responsive answers.
- **Persistent Vector Storage**: Powered by ChromaDB on local disk so document vectors survive server restarts without re-embedding.
- **Production-Ready REST API**: Fully exposed via FastAPI with auto-generated interactive OpenAPI/Swagger documentation.

---

## 🏗️ Architecture & Pipeline

```text
       [ PDF Document ]
              │
              ▼
  1. document_loader.py    ──► Extracts raw text page-by-page (pypdf)
              │
              ▼
  2. text_splitter.py      ──► Slices text into 500-char chunks (100-char overlap)
              │
              ▼
  3. embeddings.py         ──► Generates 384-dim dense vectors (all-MiniLM-L6-v2)
              │
              ▼
  4. vector_store.py       ──► Persists chunks + vectors to ChromaDB (upsert)
              │
              ▼
  5. rag_pipeline.py       ──► Embeds question, retrieves Top-K chunks & queries LLM
              │
              ▼
  6. api.py (FastAPI)      ──► Exposes REST endpoints (/health, /ingest, /ask)
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Core runtime |
| **API Framework** | FastAPI + Uvicorn | High-performance asynchronous REST API |
| **Document Loader** | PyPDF | Local PDF text and metadata extraction |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) | Local 384-dimensional vector embedding generation |
| **Vector Database** | ChromaDB | Local disk-persisted vector store and similarity search |
| **LLM Inference** | Groq API (`qwen/qwen3.8-27b`) | Fast context-augmented question answering |
| **Environment** | `python-dotenv` | Secure environment variable configuration |

---

## 📁 Project Structure

```text
documind-ai/
├── src/
│   ├── document_loader.py    # Extracts text & page metadata from PDFs
│   ├── text_splitter.py      # Slices pages into sliding-window overlapping chunks
│   ├── embeddings.py         # Local sentence-transformer embedding model wrapper
│   ├── vector_store.py       # ChromaDB persistent storage and vector querying
│   └── rag_pipeline.py       # Ingestion orchestration and prompt-augmented LLM query
├── data/                     # Uploaded documents directory (git-ignored)
├── chroma_db/                # Local ChromaDB vector storage (git-ignored)
├── api.py                    # FastAPI server exposing REST endpoints
├── requirements.txt          # Python package dependencies
├── .env.example              # Template for environment variables
├── .env                      # Local secret variables (git-ignored)
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- macOS / Linux / Windows
- Python 3.11+
- Groq API Key ([console.groq.com](https://console.groq.com))

### 2. Clone the Repository
```bash
git clone https://github.com/MetaSeng/documind-ai.git
cd documind-ai
```

### 3. Create and Activate Virtual Environment
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Or on Windows:
# .\venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the template and add your Groq API key:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### 6. Run the FastAPI Server
```bash
uvicorn api:app --reload --port 8000
```

The server will be live at `http://127.0.0.1:8000`.

---

## 📖 API Endpoints & Usage

Once the server is running, navigate to **`http://localhost:8000/docs`** for interactive Swagger UI documentation.

### 1. Health Check
- **Endpoint:** `GET /health`
- **Response:**
  ```json
  {
    "status": "ok",
    "message": "DocuMind AI API is running!"
  }
  ```

### 2. Ingest Document
Uploads a PDF, splits it into chunks, generates vector embeddings, and stores them in ChromaDB.
- **Endpoint:** `POST /ingest`
- **Content-Type:** `multipart/form-data`
- **Example cURL:**
  ```bash
  curl -X POST http://localhost:8000/ingest \
    -F "file=@data/sample.pdf"
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "message": "'sample.pdf' has been ingested successfully.",
    "saved_to": "data/sample.pdf"
  }
  ```

### 3. Ask a Question
Performs semantic similarity search against indexed document chunks, builds a contextual prompt, and queries the LLM.
- **Endpoint:** `POST /ask`
- **Content-Type:** `application/json`
- **Example Request:**
  ```json
  {
    "question": "What is DNS?",
    "top_k": 3
  }
  ```
- **Example Response:**
  ```json
  {
    "question": "What is DNS?",
    "answer": "DNS, or the Domain Name System, is described as the \"Phonebook of the Internet.\" It automatically translates friendly domain names (like example.com) into IP addresses (such as 93.184.216.34) whenever you click a link or type a web address."
  }
  ```

---

## 🗺️ Roadmap & Future Enhancements

- [ ] **Streamlit Web UI (`app.py`)**: Interactive drag-and-drop file upload and conversational chat interface.
- [ ] **Source Citations in Responses**: Returning exact page numbers alongside answers.
- [ ] **Multi-Document Namespacing**: Support isolated collections per uploaded document.
- [ ] **Async Ingestion**: Offload heavy document processing to FastAPI background worker tasks.
- [ ] **Conversation Memory**: Support contextual multi-turn conversation history.

---

## 📄 License

This project is licensed under the MIT License.

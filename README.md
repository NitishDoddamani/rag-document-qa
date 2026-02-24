# 📄 RAG Document Q&A

A full-stack AI-powered document question answering system built with **FastAPI**, **React**, and local LLMs via **Ollama**.  
Upload any PDF and ask questions — answers are grounded strictly in your document content with zero hallucination.

---

## 🖥️ Application Demo (UI Screenshots)

📌 **1️⃣ Upload Interface**
<p align="center"> <img src="images/page1.jpg" width="80%" /> </p>

Clean and minimal interface allowing users to upload PDF documents.

📤 **2️⃣ Upload in Progress**
<p align="center"> <img src="images/page2.jpg" width="80%" /> </p>

Displays real-time upload status while processing the document.

✅ **3️⃣ Document Successfully Processed**
<p align="center"> <img src="images/page3.jpg" width="80%" /> </p>

Confirms successful upload and shows number of semantic chunks generated.

💬 **4️⃣ Asking a Question**
<p align="center"> <img src="images/page4.jpg" width="80%" /> </p>

User enters a natural language question related to the uploaded PDF.

⏳ **5️⃣ LLM Thinking State**
<p align="center"> <img src="images/page5.jpg" width="80%" /> </p>

Displays progress bar while the model retrieves context and generates answer.

📚 **6️⃣ Generated Answer (Grounded Response)**
<p align="center"> <img src="images/page6.jpg" width="80%" /> </p>

Structured, markdown-formatted answer generated strictly from document content.

🔎 **7️⃣ Continued Detailed Response**
<p align="center"> <img src="images/page7.jpg" width="80%" /> </p>

Comprehensive comparison of LAN, MAN, and WAN including characteristics, advantages, and limitations.

> **Note**: The system extracts text using pdfplumber, chunks it semantically, embeds with sentence-transformers, stores in ChromaDB, and generates answers with strict grounding via Ollama.

---

## 🚀 Features

- 📤 Upload PDF documents and process them into semantic chunks
- 🔍 Semantic search using sentence-transformers embeddings
- 🤖 Local LLM inference via Ollama (no API key needed, runs fully offline)
- 🛡️ Hallucination detection and off-topic question filtering
- 📝 Markdown-formatted structured answers with headings and bullet points
- ⚡ GPU-accelerated embeddings (CUDA supported)
- 🗂️ ChromaDB vector store for fast similarity search
- 📊 Similarity scores and citation tracking per answer
- 🐳 Fully containerized with Docker and Docker Compose

---

## 🏗️ Tech Stack

| Layer            | Technology                               |
|------------------|------------------------------------------|
| Backend          | Python, FastAPI                          |
| LLM              | Ollama (command-r7b / llama3.2)          |
| Embeddings       | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB        | ChromaDB                                 |
| PDF Parsing      | pdfplumber                               |
| Frontend         | React, Axios, react-markdown             |
| Containerization | Docker, Docker Compose                   |

---

## 📁 Project Structure

```
rag-document-qa/
├── docker-compose.yml            # Orchestrates backend + frontend
├── backend/
│   ├── Dockerfile                # Backend container
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── routers/
│       │   ├── document.py       # Upload endpoint
│       │   └── query.py          # Question answering endpoint
│       └── services/
│           ├── pdf_service.py    # PDF extraction + chunking
│           ├── embedding_service.py  # Embeddings + ChromaDB
│           └── llm_service.py    # Ollama LLM + prompt engineering
├── frontend/
│   ├── Dockerfile                # Frontend container (nginx)
│   ├── .env                      # REACT_APP_API_URL
│   └── src/
│       ├── App.js
│       └── App.css
└── images/                       # Demo screenshots
    ├── page1.jpg ... page7.jpg
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) installed
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- CUDA (optional, for GPU acceleration)

---

### 🐳 Option 1 — Run with Docker (Recommended)

The easiest way to run the full stack with a single command.

**Step 1 — Clone the repository**
```bash
git clone https://github.com/NitishDoddamani/rag-document-qa.git
cd rag-document-qa
```

**Step 2 — Start Ollama on your machine**
```bash
ollama serve
ollama pull command-r7b
```

**Step 3 — Run everything with Docker Compose**
```bash
docker-compose up --build
```

Both services start automatically:

| Service  | URL                       |
|----------|---------------------------|
| Frontend | http://localhost:3000      |
| Backend  | http://localhost:8000      |
| API Docs | http://localhost:8000/docs |

**To stop:**
```bash
docker-compose down
```

---

### 💻 Option 2 — Run Manually (Without Docker)

**Step 1 — Clone & setup backend**
```bash
git clone https://github.com/NitishDoddamani/rag-document-qa.git
cd rag-document-qa/backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Step 2 — Setup frontend**
```bash
cd ../frontend
npm install
npm start
```

---

## 🔌 API Endpoints

| Method | Endpoint            | Description                       |
|--------|---------------------|-----------------------------------|
| POST   | `/documents/upload` | Upload a PDF document             |
| POST   | `/query/ask`        | Ask a question about the document |
| GET    | `/health`           | Health check                      |

### Example Response

```json
{
  "question": "What is a LAN?",
  "answer": "## LAN (Local Area Network)\n\n- Covers up to 1 km...",
  "chunks_used": 5,
  "hallucination_risk": "LOW",
  "grounded": true
}
```

---

## 🧠 How It Works

```
User uploads PDF
      ↓
PDF text extracted (pdfplumber)
      ↓
Text split into semantic chunks (overlap-aware)
      ↓
Chunks converted to embeddings (sentence-transformers)
      ↓
Embeddings stored in ChromaDB
      ↓
User asks a question
      ↓
Question embedded → similarity search in ChromaDB
      ↓
Top chunks retrieved with similarity scores
      ↓
Chunks + question sent to Ollama LLM with strict prompt
      ↓
Formatted markdown answer returned to user
```

---

## 🛡️ Hallucination Prevention

- **Strict prompt engineering** — LLM only uses provided context
- **Similarity threshold filtering** — low-score chunks are rejected
- **Off-topic question rejection** — unrelated questions return a clear message
- **Post-response grounding check** — response verified for out-of-context phrases

---

## 🐳 Docker Architecture

```
docker-compose up
      ├── backend (FastAPI on port 8000)
      │     └── connects to Ollama on host
      │           via host.docker.internal:11434
      └── frontend (React → nginx on port 3000)
```

ChromaDB data persists across restarts via a named Docker volume (`chroma_data`).

---

## 🔮 Future Improvements

- [ ] Cloud deployment (Render / Railway)
- [ ] Support for .docx Word files
- [ ] OCR for scanned/image-based PDFs
- [ ] Multi-document RAG support
- [ ] Chat history / conversation memory
- [ ] Reranking layer for better retrieval
- [ ] Authentication and user sessions

---

## 👨‍💻 Author

**Nitish Doddamani**  
[GitHub Profile](https://github.com/NitishDoddamani)

---

## 📄 License

MIT License

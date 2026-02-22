# 📄 RAG Document Q&A

A full-stack AI-powered document question answering system built with **FastAPI**, **React**, and local LLMs via **Ollama**.  
Upload any PDF and ask questions — answers are grounded strictly in your document content with zero hallucination.

🖥️ Application Demo (UI Screenshots)

📌 1️⃣ Upload Interface
<p align="center"> <img src="images/page1.jpg" width="80%" /> </p>

Description:
Clean and minimal interface allowing users to upload PDF documents.

📤 2️⃣ Upload in Progress
<p align="center"> <img src="images/page2.jpg" width="80%" /> </p>

Description:
Displays real-time upload status while processing the document.

✅ 3️⃣ Document Successfully Processed
<p align="center"> <img src="images/page3.jpg" width="80%" /> </p>

Description:
Confirms successful upload and shows number of semantic chunks generated.

💬 4️⃣ Asking a Question
<p align="center"> <img src="images/page4.jpg" width="80%" /> </p>

Description:
User enters a natural language question related to the uploaded PDF.

⏳ 5️⃣ LLM Thinking State
<p align="center"> <img src="images/page5.jpg" width="80%" /> </p>

Description:
Displays progress bar while the model retrieves context and generates answer.

📚 6️⃣ Generated Answer (Grounded Response)
<p align="center"> <img src="images/page6.jpg" width="80%" /> </p>

Description:
Structured, markdown-formatted answer generated strictly from document content.

🔎 7️⃣ Continued Detailed Response
<p align="center"> <img src="images/page7.jpg" width="80%" /> </p>

Description:
Comprehensive comparison of LAN, MAN, and WAN including characteristics, advantages, and limitations.

> **Note**: The system extracts text using pdfplumber, chunks it semantically, embeds with sentence-transformers, stores in ChromaDB, and generates answers with strict grounding via Ollama.

## 🚀 Features

- 📤 Upload PDF documents and process them into semantic chunks
- 🔍 Semantic search using sentence-transformers embeddings
- 🤖 Local LLM inference via Ollama (no API key needed, runs fully offline)
- 🛡️ Hallucination detection and off-topic question filtering
- 📝 Markdown-formatted structured answers with headings and bullet points
- ⚡ GPU-accelerated embeddings (CUDA supported)
- 🗂️ ChromaDB vector store for fast similarity search
- 📊 Similarity scores and citation tracking per answer

## 🏗️ Tech Stack

| Layer          | Technology                              |
|----------------|-----------------------------------------|
| Backend        | Python, FastAPI                         |
| LLM            | Ollama (command-r7b / llama3.2)         |
| Embeddings     | sentence-transformers (all-MiniLM-L6-v2)|
| Vector DB      | ChromaDB                                |
| PDF Parsing    | pdfplumber                              |
| Frontend       | React, Axios, react-markdown            |

## 📁 Project Structure

```
rag-document-qa/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── document.py       # Upload endpoint
│   │   │   └── query.py          # Question answering endpoint
│   │   └── services/
│   │       ├── pdf_service.py    # PDF extraction + chunking
│   │       ├── embedding_service.py  # Embeddings + ChromaDB
│   │       └── llm_service.py    # Ollama LLM + prompt engineering
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.js
│       └── App.css
└── images/                       # Demo screenshots / PDF pages
    ├── page1.jpg
    ├── page2.jpg
    ├── page3.jpg
    ├── page4.jpg
    ├── page5.jpg
    ├── page6.jpg
    └── page7.jpg
```

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) installed
- CUDA (optional, for GPU acceleration)

### 1. Clone the repository
```bash
git clone https://github.com/NitishDoddamani/rag-document-qa.git
cd rag-document-qa
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 3. Pull Ollama Model
```bash
ollama pull command-r7b
# or lighter model:
# ollama pull llama3.2:1b
```

### 4. Start Backend
```bash
uvicorn app.main:app --reload
```
Backend runs at `http://127.0.0.1:8000`

### 5. Frontend Setup
```bash
cd ../frontend
npm install
npm start
```
Frontend runs at `http://localhost:3000`

## 🔌 API Endpoints

| Method | Endpoint              | Description                     |
|--------|-----------------------|---------------------------------|
| POST   | `/documents/upload`   | Upload a PDF document           |
| POST   | `/query/ask`          | Ask a question about the document |
| GET    | `/health`             | Health check                    |

### Example Requests

```bash
# Upload document
curl -X POST "http://127.0.0.1:8000/documents/upload" \
  -F "file=@lecs110.pdf"

# Ask question
curl -X POST "http://127.0.0.1:8000/query/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a node in a computer network?"}'
```

## 🛡️ Hallucination Prevention

Multi-layer protection:
- Strict prompt engineering (LLM only uses provided context)
- Similarity threshold filtering
- Off-topic question rejection
- Post-response grounding check

## 🔮 Future Improvements

- [ ] Docker + cloud deployment
- [ ] Support for .docx files
- [ ] OCR for scanned PDFs
- [ ] Multi-document RAG
- [ ] Chat history / conversation memory
- [ ] Reranking for better retrieval

## 👨‍💻 Author

**Nitish Doddamani**  
[GitHub Profile](https://github.com/NitishDoddamani)

## 📄 License

MIT License
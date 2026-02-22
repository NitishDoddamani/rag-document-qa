import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [docUploaded, setDocUploaded] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF file!");
    
    const formData = new FormData();
    formData.append("file", file);
    
    setUploadStatus("Uploading...");
    
    try {
      const res = await axios.post("http://127.0.0.1:8000/documents/upload", formData);
      setUploadStatus(`✅ Uploaded! ${res.data.num_chunks} chunks processed`);
      setDocUploaded(true);
    } catch (err) {
      setUploadStatus("❌ Upload failed. Try again.");
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return alert("Please enter a question!");
    
    setLoading(true);
    setAnswer("");
    
    try {
      const res = await axios.post("http://127.0.0.1:8000/query/ask", { question });
      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer("❌ Error getting answer. Try again.");
    }
    
    setLoading(false);
  };

  return (
    <div className="app">
      <h1>📄 RAG Document Q&A</h1>
      <p className="subtitle">Upload a PDF and ask questions about it</p>

      <div className="card">
        <h2>📤 Upload Document</h2>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={handleUpload}>Upload PDF</button>
        {uploadStatus && <p className="status">{uploadStatus}</p>}
      </div>

      {docUploaded && (
        <div className="card">
          <h2>💬 Ask a Question</h2>
          <input
            type="text"
            placeholder="Ask something about your document..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          />
          <button onClick={handleAsk} disabled={loading}>
            {loading ? "Thinking..." : "Ask"}
          </button>

          {loading && (
            <div className="loading-bar">
              <div className="loading-fill"></div>
            </div>
          )}

          {answer && (
            <div className="answer">
              <h3>Answer:</h3>
              <div className="markdown-body">
                <ReactMarkdown>{answer}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
# 🤖 JobFit AI Agent

An AI-powered resume analyzer that matches your resume against job descriptions and gives intelligent feedback using LangGraph, Groq & FAISS.

---

## 🚀 Features
- 📄 Upload your resume and job description
- 🧠 AI analyzes skill gaps and fit score
- ⚡ Fast inference using Groq LLM
- 🔍 Semantic search powered by FAISS
- 🔄 Multi-step reasoning with LangGraph agents

---

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Agent Framework | LangGraph |
| LLM | Groq (LLaMA 3) |
| Vector Search | FAISS |
| Backend | FastAPI |
| Containerization | Docker |
| Language | Python 3.10+ |

---

## ⚙️ How to Run

### 1. Clone the repo
```bash
git clone https://github.com/akashkatakam-2004/jobfit-ai-agent.git
cd jobfit-ai-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
# Add your GROQ_API_KEY inside .env
```

### 4. Run with Docker
```bash
docker-compose up --build
```

### 5. Or run locally
```bash
uvicorn main:app --reload
```

---

## 📁 Project Structure
```
jobfit-ai-agent/
├── main.py
├── agent/
├── vector_store/
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 📜 License
MIT License

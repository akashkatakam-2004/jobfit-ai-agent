# 🎯 JobFit AI Agent

> Upload your resume + paste a job description → get match score, skill gaps, resume tips, and a cover letter — all powered by AI.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)
![Groq](https://img.shields.io/badge/Groq-LLM-purple)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![HuggingFace](https://img.shields.io/badge/🤗-HuggingFace%20Space-yellow)

---

## 🚀 Live Demo
👉 [Try it on Hugging Face Spaces](https://huggingface.co/spaces/Akashkatakam/jobfit-ai-agent)

---

## ✨ Features

- 📄 **Resume Parsing** — Extracts text from uploaded PDF resumes
- 🔍 **JD Analysis** — Paste job description text or provide a URL
- 🧠 **AI Skill Extraction** — LLM extracts skills from both resume and JD
- 📊 **FAISS Semantic Matching** — Vector similarity match score
- 📝 **Fit Report** — 3-sentence professional career coach analysis
- 💡 **Resume Tips** — 4 specific, actionable improvement suggestions
- ✉️ **Cover Letter Generator** — Auto-generated professional cover letter

---

## 🏗️ Architecture

```
PDF Resume ──┐
             ├──▶ LangGraph Agent Pipeline
Job Desc ────┘
                  ├── Node 1: Parse Resume
                  ├── Node 2: Parse JD
                  ├── Node 3: Extract Resume Skills (Groq LLM)
                  ├── Node 4: Extract JD Skills (Groq LLM)
                  ├── Node 5: FAISS Semantic Matching
                  ├── Node 6: Generate Fit Report
                  ├── Node 7: Generate Resume Tips
                  └── Node 8: Generate Cover Letter
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| AI Agent | LangGraph + LangChain |
| LLM | Groq (LLaMA 3.3 70B) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| PDF Parsing | PyMuPDF (fitz) |
| Scraping | BeautifulSoup4 |
| Deployment | Docker + HuggingFace Spaces |

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/Akashkatakam/jobfit-ai-agent.git
cd jobfit-ai-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

> 🔑 Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
python main.py
```

Open your browser at `http://localhost:7860`

---

## 🐳 Docker Setup

```bash
docker build -t jobfit-ai-agent .
docker run -p 7860:7860 -e GROQ_API_KEY=your_key_here jobfit-ai-agent
```

---

## 📂 Project Structure

```
jobfit-ai-agent/
├── main.py          # FastAPI app & API endpoints
├── agent.py         # LangGraph agent with 8 nodes
├── utils.py         # PDF extraction & URL scraping
├── config.py        # Configuration & env variables
├── requirements.txt # Python dependencies
├── Dockerfile       # Container setup
├── .env.example     # Environment variable template
└── README.md        # You are here
```

---

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |

---

## 👨‍💻 Built by

**Akash Katakam** — [Hugging Face](https://huggingface.co/Akashkatakam)

---

## 📄 License

MIT License — feel free to use, modify, and share!

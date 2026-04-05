from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn, os

from agent import build_agent
from utils import extract_pdf_text, scrape_job_url
from config import HOST, PORT

BASE_DIR  = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
    FRONTEND_HTML = f.read()

app = FastAPI(title="JobFit AI Agent")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
def root():
    return FRONTEND_HTML

@app.post("/analyze")
async def analyze(
    resume:     UploadFile = File(...),
    jd_input:   str        = Form(...),
    input_type: str        = Form(default="text")
):
    pdf_bytes   = await resume.read()
    resume_text = extract_pdf_text(pdf_bytes)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    jd_text = scrape_job_url(jd_input) if input_type == "url" else jd_input
    if not jd_text:
        raise HTTPException(status_code=400, detail="Job description is empty.")

    try:
        agent  = build_agent()
        result = agent.invoke({
            "resume_text":    resume_text,
            "jd_text":        jd_text,
            "resume_skills":  [],
            "jd_skills":      [],
            "match_score":    0.0,
            "skill_gaps":     [],
            "matched_skills": [],
            "fit_report":     "",
            "resume_tips":    [],
            "cover_letter":   "",
        })
    except Exception as e:
        err = str(e).lower()
        if "401" in err or "authentication" in err or "api key" in err:
            raise HTTPException(status_code=400, detail="Invalid Groq API key. Check your HuggingFace Space secret.")
        elif "429" in err or "rate limit" in err:
            raise HTTPException(status_code=400, detail="Rate limit hit. Wait 1 minute and try again.")
        else:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return {
        "match_score":     result["match_score"],
        "matched_skills":  result["matched_skills"],
        "skill_gaps":      result["skill_gaps"],
        "fit_report":      result["fit_report"],
        "resume_tips":     result["resume_tips"],
        "cover_letter":    result["cover_letter"],
        "jd_skills_count": len(result["jd_skills"]),
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT)

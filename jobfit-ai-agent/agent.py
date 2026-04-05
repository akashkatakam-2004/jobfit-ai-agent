"""
agent.py — LangGraph Agent
All 8 nodes: resume parse, JD scrape, skill extract, FAISS match,
fit report, resume tips, cover letter.
"""

import re
import json
from typing import TypedDict

import requests as req
from bs4 import BeautifulSoup
import fitz  # PyMuPDF

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langgraph.graph import StateGraph, END

from config import GROQ_API_KEY, GROQ_MODEL, EMBED_MODEL


# ── Agent State ────────────────────────────────────────────────
class AgentState(TypedDict):
    resume_text:    str
    jd_text:        str
    resume_skills:  list
    jd_skills:      list
    match_score:    float
    skill_gaps:     list
    matched_skills: list
    fit_report:     str
    resume_tips:    list
    cover_letter:   str


# ── Shared helpers ─────────────────────────────────────────────
def get_llm():
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0.3,
        groq_api_key=GROQ_API_KEY
    )

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def parse_json_list(raw: str) -> list:
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        return [s.strip().strip('"') for s in raw.strip("[]").split(",") if s.strip()]


# ── Node 1 & 2: Passthrough (data already injected by API) ─────
def node_passthrough(state: AgentState) -> AgentState:
    return state


# ── Node 3: Extract skills from resume ────────────────────────
def node_extract_resume_skills(state: AgentState) -> AgentState:
    llm    = get_llm()
    prompt = f"""Extract ALL technical skills, tools, frameworks from this resume.
Return ONLY a JSON array of strings. No explanation. No markdown.
Resume:\n{state['resume_text'][:3000]}"""
    skills = parse_json_list(llm.invoke(prompt).content.strip())
    return {**state, "resume_skills": skills}


# ── Node 4: Extract skills from JD ────────────────────────────
def node_extract_jd_skills(state: AgentState) -> AgentState:
    llm    = get_llm()
    prompt = f"""Extract ALL required technical skills, tools, technologies from this job description.
Return ONLY a JSON array of strings. No explanation. No markdown.
Job Description:\n{state['jd_text'][:3000]}"""
    skills = parse_json_list(llm.invoke(prompt).content.strip())
    return {**state, "jd_skills": skills}


# ── Node 5: FAISS semantic matching ───────────────────────────
def node_match_skills(state: AgentState) -> AgentState:
    resume_skills = state["resume_skills"]
    jd_skills     = state["jd_skills"]

    if not resume_skills or not jd_skills:
        return {**state, "match_score": 0.0, "matched_skills": [], "skill_gaps": jd_skills}

    embeddings  = get_embeddings()
    faiss_store = FAISS.from_texts(resume_skills, embeddings)
    matched, gaps = [], []

    for skill in jd_skills:
        results = faiss_store.similarity_search_with_score(skill, k=1)
        if results and results[0][1] < 0.8:
            matched.append(skill)
        else:
            gaps.append(skill)

    score = round((len(matched) / len(jd_skills)) * 100, 1) if jd_skills else 0.0
    return {**state, "match_score": score, "matched_skills": matched, "skill_gaps": gaps}


# ── Node 6: Generate fit report ───────────────────────────────
def node_generate_report(state: AgentState) -> AgentState:
    llm    = get_llm()
    prompt = f"""You are an expert career coach. Write a 3-sentence professional fit analysis.
Match score: {state['match_score']}%
Matched: {state['matched_skills']}
Gaps: {state['skill_gaps']}
Be honest, specific, encouraging. Flowing prose only — no bullet points."""
    return {**state, "fit_report": llm.invoke(prompt).content.strip()}


# ── Node 7: Generate resume tips ──────────────────────────────
def node_generate_tips(state: AgentState) -> AgentState:
    llm    = get_llm()
    prompt = f"""Give exactly 4 specific actionable resume improvement tips based on these gaps.
Return ONLY a JSON array of 4 strings. No markdown.
Skill gaps: {state['skill_gaps']}
Candidate has: {state['resume_skills']}"""
    tips = parse_json_list(llm.invoke(prompt).content.strip())
    return {**state, "resume_tips": tips}


# ── Node 8: Generate cover letter ─────────────────────────────
def node_generate_cover_letter(state: AgentState) -> AgentState:
    llm    = get_llm()
    prompt = f"""Write a professional 3-paragraph cover letter.
Candidate skills: {state['resume_skills'][:15]}
Job requirements: {state['jd_skills'][:15]}
Match score: {state['match_score']}%
Use "your organization" not placeholders. Warm but professional tone."""
    return {**state, "cover_letter": llm.invoke(prompt).content.strip()}


# ── Build LangGraph ────────────────────────────────────────────
def build_agent():
    wf = StateGraph(AgentState)

    wf.add_node("parse_resume",          node_passthrough)
    wf.add_node("scrape_jd",             node_passthrough)
    wf.add_node("extract_resume_skills", node_extract_resume_skills)
    wf.add_node("extract_jd_skills",     node_extract_jd_skills)
    wf.add_node("match_skills",          node_match_skills)
    wf.add_node("generate_report",       node_generate_report)
    wf.add_node("generate_tips",         node_generate_tips)
    wf.add_node("generate_cover_letter", node_generate_cover_letter)

    wf.set_entry_point("parse_resume")
    wf.add_edge("parse_resume",          "scrape_jd")
    wf.add_edge("scrape_jd",             "extract_resume_skills")
    wf.add_edge("extract_resume_skills", "extract_jd_skills")
    wf.add_edge("extract_jd_skills",     "match_skills")
    wf.add_edge("match_skills",          "generate_report")
    wf.add_edge("generate_report",       "generate_tips")
    wf.add_edge("generate_tips",         "generate_cover_letter")
    wf.add_edge("generate_cover_letter", END)

    return wf.compile()

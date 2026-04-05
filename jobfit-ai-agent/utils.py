"""
utils.py — Helper functions
PDF text extraction and job URL scraping.
"""

import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract all text from a PDF file given as bytes."""
    doc  = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text.strip()


def scrape_job_url(url: str) -> str:
    """Fetch and clean text from a job posting URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp    = requests.get(url, headers=headers, timeout=10)
        soup    = BeautifulSoup(resp.text, "html.parser")

        # Remove noise tags
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()

        lines = [l.strip() for l in soup.get_text(separator="\n").splitlines() if l.strip()]
        return "\n".join(lines[:200])

    except Exception as e:
        return f"Could not scrape URL: {e}"

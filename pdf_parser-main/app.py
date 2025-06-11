import re
import json
import fitz                  # PyMuPDF
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# ——— Your existing regexes & helpers ———
PAGE_ISSUE_RE = re.compile(r'Page.*Issue')
DOC_NUM_RE    = re.compile(r'^LEAP-1B-')
HEADER_RE     = re.compile(r'New Part Number /|Qty Unit \$|List of spares', re.IGNORECASE)

def clean_text(text: str) -> str:
    return "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
        and not PAGE_ISSUE_RE.search(line)
        and not DOC_NUM_RE.match(line.strip())
        and not HEADER_RE.search(line)
    )

def extract_text(path: Path) -> str:
    doc = fitz.open(str(path))
    pages = [p.get_text("text") for p in doc if p.get_text("text")]
    doc.close()
    return clean_text("\n".join(pages))

def detect_engine(filename: str) -> str:
    return "cfm" if "cfm" in filename.lower() else "leap"

# ——— FastAPI setup ———
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # for production, restrict to your front-end domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse")
async def parse_pdf(file: UploadFile = File(...)):
    tmp = Path("/tmp") / file.filename
    with open(tmp, "wb") as f:
        f.write(await file.read())

    engine = detect_engine(file.filename)
    text   = extract_text(tmp)
    return {"filename": file.filename, "engine": engine, "text_preview": text[:500]}

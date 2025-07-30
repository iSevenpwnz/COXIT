import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
import pdfplumber

import openai
from dotenv import load_dotenv

MAX_FILE_SIZE_MB = 50
MAX_PAGES = 100
PDFS_DIR = os.path.join(os.path.dirname(__file__), "..", "storage", "pdfs")
SUMMARIES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "storage", "summaries"
)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
META_DIR = os.path.join(os.path.dirname(__file__), "..", "storage", "meta")
META_PATH = os.path.join(META_DIR, "metadata.json")
import json
from datetime import datetime


def get_summary_via_openai(text: str) -> str:
    if not OPENAI_API_KEY:
        return "OpenAI API key not set"

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    # Тримати prompt коротким, обрізати текст якщо треба
    prompt = (
        "Стисло підсумуй цей документ українською мовою (до 500 слів):\n\n"
        + text[:12000]
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI error: {e}"


def parse_pdf(file_path: str):
    # Текст
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception:
        text = ""
    # Зображення
    images = 0
    try:
        doc = fitz.open(file_path)
        for page in doc:
            images += len(page.get_images(full=True))
    except Exception:
        images = 0
    # Таблиці (рахуємо кількість таблиць через pdfplumber)
    tables = 0
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                tables += len(page.extract_tables())
    except Exception:
        tables = 0
    return {"text": text, "images": images, "tables": tables}


app = FastAPI()

# Додаємо CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Перевірка типу
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Тільки PDF-файли підтримуються"
        )
    # Перевірка розміру
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400, detail="PDF занадто великий (макс 50 МБ)"
        )
    # Перевірка кількості сторінок
    try:
        from io import BytesIO

        reader = PdfReader(BytesIO(contents))
        num_pages = len(reader.pages)
    except Exception:
        raise HTTPException(status_code=400, detail="Не вдалося прочитати PDF")
    if num_pages > MAX_PAGES:
        raise HTTPException(
            status_code=400, detail="PDF має більше 100 сторінок"
        )
    # Збереження
    os.makedirs(PDFS_DIR, exist_ok=True)
    os.makedirs(SUMMARIES_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(PDFS_DIR, f"{file_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(contents)
    # Парсинг PDF
    parsed = parse_pdf(file_path)
    # Генерація summary через OpenAI
    summary = get_summary_via_openai(parsed["text"])
    # Зберігаємо summary
    summary_path = os.path.join(SUMMARIES_DIR, f"{file_id}.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    # Зберігаємо метадані
    os.makedirs(META_DIR, exist_ok=True)
    meta = {
        "id": file_id,
        "filename": f"{file_id}.pdf",
        "summary_file": f"{file_id}.txt",
        "created_at": datetime.utcnow().isoformat(),
        "pages": num_pages,
        "size_mb": round(size_mb, 2),
        "text_length": len(parsed["text"]),
        "images": parsed["images"],
        "tables": parsed["tables"],
    }
    # Додаємо в metadata.json (append, max 1000 записів)
    try:
        if os.path.exists(META_PATH):
            with open(META_PATH, "r", encoding="utf-8") as f:
                all_meta = json.load(f)
        else:
            all_meta = []
        all_meta.append(meta)
        all_meta = all_meta[-1000:]
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(all_meta, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pass
    return {
        "id": file_id,
        "pages": num_pages,
        "size_mb": round(size_mb, 2),
        "text_length": len(parsed["text"]),
        "images": parsed["images"],
        "tables": parsed["tables"],
        "summary": summary,
    }


@app.get("/history")
def get_history():
    # Повертаємо останні 5 записів з metadata.json
    try:
        if os.path.exists(META_PATH):
            with open(META_PATH, "r", encoding="utf-8") as f:
                all_meta = json.load(f)
            history = all_meta[-5:][::-1]
        else:
            history = []
    except Exception:
        history = []
    return {"history": history}


@app.get("/download/{summary_id}")
def download_summary(summary_id: str):
    summary_path = os.path.join(SUMMARIES_DIR, f"{summary_id}.txt")
    if not os.path.exists(summary_path):
        raise HTTPException(status_code=404, detail="Summary not found")
    with open(summary_path, "r", encoding="utf-8") as f:
        summary = f.read()
    return JSONResponse(content={"summary": summary})

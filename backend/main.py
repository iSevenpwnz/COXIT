import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader

MAX_FILE_SIZE_MB = 50
MAX_PAGES = 100
PDFS_DIR = os.path.join(os.path.dirname(__file__), "..", "storage", "pdfs")

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Перевірка типу
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Тільки PDF-файли підтримуються")
    # Перевірка розміру
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="PDF занадто великий (макс 50 МБ)")
    # Перевірка кількості сторінок
    try:
        from io import BytesIO
        reader = PdfReader(BytesIO(contents))
        num_pages = len(reader.pages)
    except Exception:
        raise HTTPException(status_code=400, detail="Не вдалося прочитати PDF")
    if num_pages > MAX_PAGES:
        raise HTTPException(status_code=400, detail="PDF має більше 100 сторінок")
    # Збереження
    os.makedirs(PDFS_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(PDFS_DIR, f"{file_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(contents)
    return {"id": file_id, "pages": num_pages, "size_mb": round(size_mb, 2)}

@app.get("/history")
def get_history():
    # TODO: return last 5 processed PDFs
    return {"history": []}

@app.get("/download/{summary_id}")
def download_summary(summary_id: str):
    # TODO: return summary file by id
    return JSONResponse(content={"message": "Download endpoint заглушка"})
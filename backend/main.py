from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # TODO: validate and save file, parse, summarize
    return {"message": "Upload endpoint заглушка"}

@app.get("/history")
def get_history():
    # TODO: return last 5 processed PDFs
    return {"history": []}

@app.get("/download/{summary_id}")
def download_summary(summary_id: str):
    # TODO: return summary file by id
    return JSONResponse(content={"message": "Download endpoint заглушка"})
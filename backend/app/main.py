curl -X POST "http://localhost:8000/upload" \
  -F "file=@test.pdf.pdf"from fastapi import FastAPI, UploadFile, File
import os
import base64

UPLOAD_DIR = "uploads"

app = FastAPI()


@app.get("/")
def home():
    return {"AIxRPA API radi! :)"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    content = await file.read()

    pdf_base64 = base64.b64encode(content).decode("utf-8")

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "base64length": len(pdf_base64)
    }



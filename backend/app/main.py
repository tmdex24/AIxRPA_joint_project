from fastapi import FastAPI, File, UploadFile
from .services.pdf_service import extract_text
from .services.qwen_service import extract_invoice_data

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

    print("PDF SACUVAN!")

    text = extract_text(file_path)

    print("PDF PROCITAN")
    print(text[:200])

    invoice_data = extract_invoice_data(text)

    print("GOTOVO")

    return {
        "filename": file.filename,
        "invoice": invoice_data
    }



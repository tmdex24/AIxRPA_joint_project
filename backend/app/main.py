from fastapi import FastAPI, File, UploadFile
from .services.pdf_service import extract_text
from .services.qwen_service import extract_invoice_data
from datetime import datetime

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

    text = extract_text(file_path)

    invoice_data = extract_invoice_data(text)

    amount = invoice_data.get("total_amount")

    if amount:
        amount = float(amount.replace(",",""))
        #izvlacim amount iz invoice data, pretvaram ga u float, jer baza zahteva decimal tip, a ne string!
        invoice_data["total_amount"] = amount

    date = invoice_data.get("date_of_issue")

    if date:
        invoice_data["date_of_issue"] = datetime.strptime(
            date,
            "%d/%m/%Y"
        ).strftime("%Y-%m-%d")


    return {
        "filename": file.filename,
        "invoice": invoice_data
    }
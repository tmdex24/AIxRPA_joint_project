from fastapi import FastAPI, File, UploadFile
from .services.pdf_service import extract_text
from .services.qwen_service import extract_invoice_data

from database.crud import (
    insert_invoice,
    update_invoice_data
)

from datetime import datetime
import uuid
import os

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

    with open(file_path, "wb") as f:
        f.write(content)

    invoice_id = str(uuid.uuid4())

    insert_invoice(
        invoice_id,
        file.filename,
        "PROCESSING"
    )

    text = extract_text(file_path)

    invoice_data = extract_invoice_data(text)

    amount = invoice_data.get("total_amount")

    if amount:
        amount = float(amount.replace(",", ""))
        invoice_data["total_amount"] = amount

    date = (
        invoice_data.get("date_of_issue")
        or invoice_data.get("date_of_issues")
    )

    if date:

    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):

        try:
            invoice_data["date_of_issue"] = (
                datetime.strptime(date, fmt)
                .strftime("%Y-%m-%d")
            )
            break

        except ValueError:
            passstrftime("%Y-%m-%d")

    update_invoice_data(
        invoice_id,
        text,
        invoice_data.get("invoice_number"),
        invoice_data.get("date_of_issue"),
        invoice_data.get("client_name"),
        invoice_data.get("client_tax_id"),
        invoice_data.get("total_amount"),
        invoice_data.get("currency"),
        "COMPLETED"
    )

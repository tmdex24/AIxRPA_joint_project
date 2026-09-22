from pydantic import BaseModel
from typing import Optional
#ugnježden (nested) Pydantic model: - jer jedna od stvari koje vraca /upload je JSON odgovor modela,
#pa je bolja praksa napraviti jednu schemu za json a jednu za odgovor konkretnog API-ja

class InvoiceData(BaseModel):
    invoice_number: Optional[str] = None
    date_of_issue: Optional[str] = None
    client_name: Optional[str] = None
    client_tax_id: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None


class UploadResponse(BaseModel):
    invoice_id: str
    filename: str
    invoice: InvoiceData
from pydantic import BaseModel
from datetime import datetime

class files(BaseModel):
    pdf_content: str

class analysis(BaseModel):
    pdf_content: str
    analysis: str
    created_at: datetime = datetime.now()
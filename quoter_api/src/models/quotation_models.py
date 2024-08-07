from pydantic import BaseModel

class QuotationInput(BaseModel):
    text: str

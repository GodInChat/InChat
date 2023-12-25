from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid

class PdfSchemaResponse(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    id: uuid.UUID
    pdf_url: str
    created_at: datetime
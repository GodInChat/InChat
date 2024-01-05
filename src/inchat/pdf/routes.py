import uuid
import io

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession

from src.inchat.auth.service import current_user
from src.inchat.database.sql.postgres import database
from src.inchat.database.sql.models import User, Pdf
from src.inchat.pdf.schemas import PdfSchemaResponse
from src.inchat.pdf.repository import PdfQuery

from src.inchat.pdf.service.local_save import save_pdf
from src.inchat.pdf.service.process import process_pdf
from src.inchat.pdf.service.vetorize import vectorize
router = APIRouter(prefix="/pdf", tags=["pdfs"])


@router.post("/upload", response_model=PdfSchemaResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(pdf_file: UploadFile, user: User = Depends(current_user),
                     db: AsyncSession = Depends(database)):
    text = process_pdf(io.BytesIO(await pdf_file.read()))
    file_name = pdf_file.filename
    await vectorize(file_name, text)
    pdf = await PdfQuery.create(file_name, user, db)
    return pdf


@router.get("/{pdf_id}", response_model=PdfSchemaResponse)
async def get_pdf(pdf_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    pdf = await PdfQuery.read(pdf_id, db)

    if not pdf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found!"
        )
    return pdf

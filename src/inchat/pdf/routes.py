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
from src.inchat.pdf.service.vectorize import vectorize


router = APIRouter(prefix="/pdf", tags=["pdfs"])


@router.post("/upload", response_model=PdfSchemaResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(pdf_file: UploadFile, user: User = Depends(current_user),
                     db: AsyncSession = Depends(database)):
    text = process_pdf(io.BytesIO(await pdf_file.read()))
    pdf = await PdfQuery.create(pdf_file.filename, user, db)
    await vectorize(str(pdf.id), text)
    return pdf

@router.get("/get_all",response_model=list[PdfSchemaResponse])
async def get_all_pdfs(user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    all_pdfs = await PdfQuery.get_all_pdfs_by_user_id(user.id, db)
    return all_pdfs


@router.get("/{pdf_id}", response_model=PdfSchemaResponse)
async def get_pdf(pdf_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    pdf = await PdfQuery.read(pdf_id, user.id, db)
    if not pdf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return pdf


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pdf(pdf_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    chat = await PdfQuery.read(pdf_id, user.id, db)
    if not chat:
        raise HTTPException(status_code=404)
    await PdfQuery.delete(chat, db)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.inchat.database.sql.models import User, Pdf
from src.inchat.pdf.schemas import PdfSchemaResponse

import uuid



class PdfQuery:
    @staticmethod
    async def create(pdf_name, user: User, session: AsyncSession) -> Pdf:
        pdf = Pdf(id= uuid.uuid4(), pdf_name=pdf_name, user_id=user.id)
        session.add(pdf)
        await session.commit()
        return pdf

    @staticmethod
    async def read(pdf_id: uuid.UUID,user_id: uuid.UUID, session: AsyncSession) -> Pdf | None:
        stmt = select(Pdf).where(Pdf.id == pdf_id, Pdf.user_id == user_id)
        pdf = await session.execute(stmt)
        return pdf.scalars().unique().one_or_none()

    @staticmethod
    async def get_all_pdfs_by_user_id(user_id: uuid.UUID, session: AsyncSession) -> list[Pdf]:
        stmt = select(Pdf).where(Pdf.user_id == user_id)
        pdfs = await session.execute(stmt)
        return list(pdfs.scalars().unique().all())

    @staticmethod
    async def delete(pdf: Pdf, session: AsyncSession) -> None:
        await session.delete(pdf)
        await session.commit()
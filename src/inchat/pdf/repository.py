from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.inchat.database.sql.models import User, Pdf
from src.inchat.pdf.schemas import PdfSchemaResponse

import uuid



class PdfQuery:
    @staticmethod
    async def create(pdf_data: list[dict], user: User, session: AsyncSession) -> list[Pdf]:
        pdfs = [Pdf(**instance, user_id=user.id) for instance in pdf_data]
        session.add_all(pdfs)
        await session.commit()
        return pdfs

    @staticmethod
    async def read(pdf_id: uuid.UUID, session: AsyncSession) -> Pdf | None:
        stmt = select(Pdf).where(Pdf.id == pdf_id)
        pdf = await session.execute(stmt)
        return pdf.scalars().unique().one_or_none()

    @staticmethod
    async def delete(pdf_id: uuid, session: AsyncSession) -> None:
        stmt = select(Pdf).where(Pdf.id == pdf_id)
        pdf = await session.execute(stmt)
        await session.delete(pdf)
        await session.commit()
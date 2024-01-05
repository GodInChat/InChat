from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.inchat.database.sql.models import User, Pdf, Chat, Message
from src.inchat.pdf.schemas import PdfSchemaResponse

import uuid



class ChatQuery:
    @staticmethod
    async def create(user_id, session: AsyncSession) -> Chat:
        chat = Chat(id=uuid.uuid4(), user_id=user_id)
        session.add(chat)
        await session.commit()
        return chat

    @staticmethod
    async def read(chat_id: uuid.UUID, session: AsyncSession) -> Chat | None:
        stmt = select(Chat).where(Chat.id == chat_id)
        chat = await session.execute(stmt)
        return chat.scalars().unique().one_or_none()


    @staticmethod
    async def append_chat_history(messages: list[Message], session: AsyncSession) -> None:
        session.add_all(messages)
        await session.commit()


    #
    # @staticmethod
    # async def delete(pdf_id: uuid, session: AsyncSession) -> None:
    #     stmt = select(Pdf).where(Pdf.id == pdf_id)
    #     pdf = await session.execute(stmt)
    #     await session.delete(pdf)
    #     await session.commit()
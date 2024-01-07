from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.inchat.database.sql.models import Chat, Message

import uuid
import datetime


class ChatQuery:
    @staticmethod
    async def create(user_id, session: AsyncSession) -> Chat:
        chat = Chat(id=uuid.uuid4(), user_id=user_id)
        session.add(chat)
        await session.commit()
        await session.refresh(chat)
        return chat

    @staticmethod
    async def read(chat_id: uuid.UUID,user_id: uuid.UUID, session: AsyncSession) -> Chat | None:
        stmt = select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
        chat = await session.execute(stmt)
        return chat.scalars().unique().one_or_none()

    @staticmethod
    async def get_all_chats_by_user_id(user_id: uuid.UUID, session: AsyncSession)-> list[Chat]:
        stmt = select(Chat).where(Chat.user_id == user_id)
        chat = await session.execute(stmt)
        return list(chat.scalars().unique().all())

    @staticmethod
    async def delete_chat(chat:Chat, session: AsyncSession) -> None:
        await session.delete(chat)
        await session.commit()


    @staticmethod
    async def append_chat_history(chat_id:uuid.UUID,messages: list[Message],times: list[datetime], session: AsyncSession) -> None:

        human_message = Message(id=uuid.uuid4(),
                                chat_id=chat_id,
                                text=messages[0],
                                owner_type="HumanMessage",
                                created_at=times[0])

        ai_message = Message(id=uuid.uuid4(),
                             chat_id=chat_id,
                             text=messages[1],
                             owner_type="AIMessage",
                             created_at=times[1])

        session.add_all([human_message, ai_message])
        await session.commit()


    #
    # @staticmethod
    # async def delete(pdf_id: uuid, session: AsyncSession) -> None:
    #     stmt = select(Pdf).where(Pdf.id == pdf_id)
    #     pdf = await session.execute(stmt)
    #     await session.delete(pdf)
    #     await session.commit()
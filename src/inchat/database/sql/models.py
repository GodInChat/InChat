import uuid

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyBaseOAuthAccountTableUUID,
)
from sqlalchemy import String, Text, Integer, DateTime, Boolean, func, Uuid, Numeric, Enum


from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")



class Pdf(Base):
    __tablename__ = "pdfs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("user.id"), nullable=True)
    pdf_name: Mapped[str] = mapped_column(String(300), nullable=False, default="placeholder")
    created_at: Mapped[DateTime] = mapped_column("crated_at", DateTime, default=func.now(), nullable=False)


class Chat(Base):
    __tablename__ = "chats"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("user.id"), nullable=True)
    created_at: Mapped[DateTime] = mapped_column("crated_at", DateTime, default=func.now(), nullable=False)

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", lazy="joined", cascade="all, delete")


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, unique=True, index=True)
    chat_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("chats.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False, default="placeholder")
    owner_type:Mapped[Enum] = mapped_column(Enum("HumanMessage", "AIMessage", name="owner_type"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column("crated_at", DateTime, default=func.now(), nullable=False)

    chat : Mapped[Chat] = relationship("Chat", back_populates="messages", lazy="noload")


class Link(Base):
    __tablename__ = "links"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, unique=True, index=True)
    link_tg: Mapped[str] = mapped_column(String(128), nullable=False)
    # user_id is not id of noname user: it is id of author who was created link
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("user.id"), nullable=True)
    pdf_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=True)
    text: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    created_at: Mapped[DateTime] = mapped_column("crated_at", DateTime, default=func.now(), nullable=False)

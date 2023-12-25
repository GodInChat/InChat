import uuid
from datetime import datetime

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyBaseOAuthAccountTableUUID,
)
from sqlalchemy import String, Integer, DateTime, Boolean, func, Uuid, Numeric


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
    pdf_url: Mapped[str] = mapped_column(String(300), nullable=False, default="placeholder")
    created_at: Mapped[DateTime] = mapped_column("crated_at", DateTime, default=func.now(), nullable=False)



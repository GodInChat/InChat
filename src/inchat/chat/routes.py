import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile

from src.inchat.database.sql.models import User, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.inchat.auth.service import current_user
from src.inchat.database.sql.postgres import database
from src.inchat.chat.schemas import InitChatSchemaResponse, NewMessageChatSchemaRespond, NewMessageChatSchemaRequest
from src.inchat.chat.repository import ChatQuery

from src.inchat.chat.service.chain import get_chain_with_retriever
router = APIRouter(prefix="/chat", tags=["chats"])


@router.post("/init", response_model=InitChatSchemaResponse, status_code=status.HTTP_201_CREATED)
async def init_chat(user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    chat = await ChatQuery.create(user.id,db)
    return chat


@router.post("/on_new_message", response_model=NewMessageChatSchemaRespond)
async def new_message(body: NewMessageChatSchemaRequest,user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    chain = get_chain_with_retriever(body.pdf_name)
    human_message = Message(id=uuid.uuid4(), chat_id=body.chat_id, text=body.human_question, owner_type="HumanMessage", created_at=datetime.now())
    chat_history = [] # todo load chat history from database
    ai_msg = chain.invoke({"question": body.human_question, "chat_history": chat_history})
    ai_message = Message(id=uuid.uuid4(), chat_id=body.chat_id, text=ai_msg, owner_type="AIMessage", created_at=datetime.now())
    await ChatQuery.append_chat_history([human_message,ai_message],db)
    return {'chat_id': body.chat_id, 'human_question': body.human_question, 'ai_answer': ai_msg}

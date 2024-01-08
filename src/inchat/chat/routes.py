import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, status

from src.inchat.database.sql.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from src.inchat.auth.service import current_user
from src.inchat.database.sql.postgres import database
from src.inchat.chat.schemas import NewMessageChatSchemaRespond, NewMessageChatSchemaRequest, ChatSchemaResponse
from src.inchat.chat.repository import ChatQuery

from src.inchat.chat.service.history import transform_chat_messages
from src.inchat.chat.service.chain import get_chain_with_retriever
router = APIRouter(prefix="/chat", tags=["chats"])


@router.post("/init", response_model=ChatSchemaResponse, status_code=status.HTTP_201_CREATED)
async def init_chat(user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    chat = await ChatQuery.create(user.id,db)
    return chat


@router.get('/get_all', response_model=list[ChatSchemaResponse])
async def get_all_chats(user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    chats = await ChatQuery.get_all_chats_by_user_id(user.id, db)
    return chats

@router.post("/new_message", response_model=NewMessageChatSchemaRespond)
async def new_message(body: NewMessageChatSchemaRequest,user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    chat = await ChatQuery.read(body.chat_id, user.id,db)
    if not chat:
        raise HTTPException(status_code=404)

    chain = get_chain_with_retriever(body.pdf_id)
    chat_history = transform_chat_messages(chat.messages)

    time_before_prompt = datetime.now()
    ai_msg = await chain.ainvoke({"question": body.human_question, "chat_history": chat_history})
    time_after_prompt = datetime.now()

    messages = [body.human_question, ai_msg]
    times = [time_before_prompt, time_after_prompt]

    await ChatQuery.append_chat_history(body.chat_id,messages,times,db)
    return {'chat_id': body.chat_id, 'human_question': body.human_question, 'ai_answer': ai_msg}

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(database)):
    chat = await ChatQuery.read(chat_id, user.id, db)
    if not chat:
        raise HTTPException(status_code=404)
    await ChatQuery.delete_chat(chat, db)
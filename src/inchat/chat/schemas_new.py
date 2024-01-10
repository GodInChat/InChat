from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class NewMessageChatSchemaRequest(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    chat_id: uuid.UUID
    human_question: str
    pdf_id: str

class NewMessageChatSchemaRespond(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    chat_id: uuid.UUID
    human_question: str
    ai_answer: str

class ChatMessageSchemaResponse(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    text: str
    owner_type: str
    created_at: datetime

class ChatSchemaResponse(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    id: uuid.UUID
    messages: list[ChatMessageSchemaResponse]
    created_at: datetime


# New schemas added


class NewMessage2ChatSchemaRequest(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    chat_id: uuid.UUID
    human_question: str
    pdf_id: str

class NewMessage2ChatSchemaRespond(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    chat_id: uuid.UUID
    human_question: str
    ai_answer: str

class ChatMessage2SchemaResponse(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    text: str
    owner_type: str
    created_at: datetime

class Chat2SchemaResponse(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    id: uuid.UUID
    messages: list[ChatMessageSchemaResponse]
    created_at: datetime





class Link2ChatSchemaRequest(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    user_id: uuid.UUID # author id
    text: str

class Link2ChatSchemaRepond(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

    user_id: uuid.UUID # author id
    text: str

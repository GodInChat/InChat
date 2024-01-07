from src.inchat.database.sql.models import Message

from langchain.schema import HumanMessage, AIMessage

def transform_chat_messages(messages: list[Message]) -> list[HumanMessage|AIMessage]:
    transformed_messages = []
    for message in messages:
        if message.owner_type == 'HumanMessage':
            transformed_messages.append(HumanMessage(content=message.text))
        elif message.owner_type == 'AIMessage':
            transformed_messages.append(AIMessage(content=message.text))
    return transformed_messages
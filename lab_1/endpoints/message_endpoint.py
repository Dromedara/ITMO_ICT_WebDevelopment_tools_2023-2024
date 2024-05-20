from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from models import MessageDefault, MessagesSubmodels, Message, ReadMessageUpdate
from db.connection import get_session

message_router = APIRouter()


@message_router.post("/create", status_code=status.HTTP_201_CREATED)
def message_create(message: MessageDefault, session=Depends(get_session)) \
        -> Message:
    message = Message.model_validate(message)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


@message_router.get("/list-in/{doing_id}", status_code=status.HTTP_200_OK)
def messages_list(doing_id: int, session=Depends(get_session)) -> list[Message]:
    return session.query(Message).filter(Message.doing_id == doing_id).all()


@message_router.get("/{message_id}", status_code=status.HTTP_200_OK,  response_model=MessagesSubmodels)
def message_get(message_id: int, session=Depends(get_session)) -> Message:
    obj = session.get(Message,  message_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="message not found")
    return obj


@message_router.patch("/update-{message_id}", status_code=status.HTTP_202_ACCEPTED)
def message_update(message_id: int, message: ReadMessageUpdate, session=Depends(get_session)) -> Message:
    db_message = session.get(Message, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="message not found")
    message_data = message.model_dump(exclude_unset=True)
    for key, value in message_data.items():
        setattr(db_message, key, value)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


@message_router.delete("/delete{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def message_delete(message_id: int, session=Depends(get_session)):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="message not found")
    session.delete(message)
    session.commit()
    return {"ok": True}

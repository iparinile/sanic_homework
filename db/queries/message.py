from typing import List

from api.request import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException, DBMessageNotExistsException
from db.models import DBMessage


def create_message(session: DBSession, message: RequestCreateMessageDto, sender_id: int) -> DBMessage:
    # Поиск по login в users
    recipient = session.get_user_by_login(message.recipient)
    if recipient is None:
        raise DBUserNotExistsException

    new_message = DBMessage(
        sender_id=sender_id,
        recipient_id=recipient.id,
        message=message.message
    )

    session.add_model(new_message)

    return new_message


def get_messages(session: DBSession, user_id: int) -> List['DBMessage']:
    return session.get_my_all_messages(user_id)


def get_db_message(session: DBSession, message_id: int) -> DBMessage:
    db_message = session.get_message_db_by_message_id(message_id)
    if db_message is None:
        raise DBMessageNotExistsException
    return db_message


def patch_message(db_message: DBMessage, edit_message: str) -> DBMessage:
    db_message.message = edit_message
    return db_message


def delete_message(db_message: DBMessage) -> DBMessage:
    db_message.is_delete = True
    return db_message

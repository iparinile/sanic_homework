from api.request import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException
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

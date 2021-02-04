from typing import List

from api.request import RequestCreateUserDto, RequestPatchUserDto
from db.database import DBSession
from db.exceptions import DBUserExistsException, DBUserNotExistsException
from db.models import DBUser


def create_user(session: DBSession, user: RequestCreateUserDto, hashed_password: bytes) -> DBUser:
    new_user = DBUser(
        login=user.login,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    if session.get_user_by_login_with_deleted(new_user.login) is not None:
        raise DBUserExistsException

    session.add_model(new_user)

    return new_user


def get_user(session: DBSession, *, login: str = None, user_id: int = None) -> DBUser:
    db_user = None

    if login is not None:
        db_user = session.get_user_by_login(login)
    elif user_id is not None:
        db_user = session.get_user_by_id(user_id)

    if db_user is None:
        raise DBUserNotExistsException
    return db_user


def patch_user(session: DBSession, user: RequestPatchUserDto, user_id: int) -> DBUser:
    db_user = session.get_user_by_id(user_id)

    for attr in user.fields:
        if hasattr(user, attr):
            value = getattr(user, attr)
            setattr(db_user, attr, value)

    return db_user


def delete_user(session: DBSession, user_id: int) -> DBUser:
    db_user = session.get_user_by_id(user_id)

    try:
        db_user.is_delete = True
    except AttributeError:
        raise DBUserNotExistsException

    return db_user


def get_users(session: DBSession) -> List['DBUser']:
    return session.get_user_all()

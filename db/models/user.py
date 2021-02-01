from sqlalchemy import Column, VARCHAR, VARBINARY, BOOLEAN

from db.models import BaseModel


class DBUser(BaseModel):

    __tablename__ = 'users'

    login = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARBINARY(), nullable=False)
    first_name = Column(VARCHAR(255))
    last_name = Column(VARCHAR(255))
    is_delete = Column(BOOLEAN(), nullable=False, default=False)

from sqlalchemy import Column, VARCHAR, Integer, ForeignKey

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    sender_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = Column(VARCHAR(), nullable=False)

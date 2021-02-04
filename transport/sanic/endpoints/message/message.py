from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.patch_message import RequestPatchMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBMessageNotExistsException, DBDataException, DBIntegrityException
from db.queries import message as message_queries

from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessageNotFound, SanicDBException


class MessageEndpoint(BaseEndpoint):

    async def method_patch(self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict,
                           *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestPatchMessageDto(body)

        try:
            db_message = message_queries.get_db_message(session, msg_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        if token.get('uid') != db_message.sender_id:
            return await self.make_response_json(status=403, message='You can only change your own data')

        db_message = message_queries.patch_message(db_message, request_model.message)

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=200)

    async def method_delete(self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict,
                            *args, **kwargs) -> BaseHTTPResponse:

        try:
            db_message = message_queries.get_db_message(session, msg_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        if token.get('uid') != db_message.sender_id:
            return await self.make_response_json(status=403, message='You can only delete your own data')

        try:
            db_message = message_queries.delete_message(db_message)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

    async def method_get(self, request: Request, body: dict, session: DBSession, msg_id: int, token: dict,
                         *args, **kwargs) -> BaseHTTPResponse:

        try:
            db_message = message_queries.get_db_message(session, msg_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFound('Message not found')

        if token.get('uid') != db_message.sender_id and token.get('uid') != db_message.recipient_id:
            return await self.make_response_json(status=403, message='You can only see your own data')

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=200)

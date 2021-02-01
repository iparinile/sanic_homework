from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseMessageDto
from db.exceptions import DBUserNotExistsException, DBDataException, DBIntegrityException
from db.queries import message as message_queries

from api.request import RequestCreateMessageDto
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicRecipientNotFound, SanicDBException


class CreateMessageEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, token: dict, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        try:
            db_message = message_queries.create_message(session, request_model, token.get('uid'))
        except DBUserNotExistsException:
            raise SanicRecipientNotFound('Recipient not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

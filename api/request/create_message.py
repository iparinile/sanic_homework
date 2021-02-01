from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    message = fields.Str(required=True, allow_none=False)
    recipient = fields.Str(required=True, allow_none=False)


class RequestCreateUserDto(RequestDto, RequestCreateMessageDtoSchema):
    __schema__ = RequestCreateMessageDtoSchema

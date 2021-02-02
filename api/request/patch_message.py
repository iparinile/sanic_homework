from marshmallow import Schema, fields

from api.base import RequestDto


class RequestPatchMessageDtoSchema(Schema):
    message = fields.Str(required=True)


class RequestPatchMessageDto(RequestDto, RequestPatchMessageDtoSchema):
    __schema__ = RequestPatchMessageDtoSchema

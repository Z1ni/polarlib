from protobuf3.fields import Int32Field, MessageField
from protobuf3.message import Message
from common import DateTime


class UserID(Message):
    pass

UserID.add_field('id', Int32Field(field_number=1, required=True))
UserID.add_field('modified', MessageField(field_number=100, required=True, message_cls=DateTime))

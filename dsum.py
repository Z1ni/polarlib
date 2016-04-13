from protobuf3.fields import Int32Field, MessageField
from protobuf3.message import Message
from common import Date, Time


class Dsum(Message):
    pass


class TimeToGo(Message):
    pass


class UnknownTimes(Message):
    pass

Dsum.add_field('date', MessageField(field_number=1, required=True, message_cls=Date))
Dsum.add_field('steps', Int32Field(field_number=2, required=True))
Dsum.add_field('timeToGo', MessageField(field_number=6, required=True, message_cls=TimeToGo))
Dsum.add_field('unkTimes', MessageField(field_number=7, required=True, message_cls=UnknownTimes))
TimeToGo.add_field('up', MessageField(field_number=3, required=True, message_cls=Time))
TimeToGo.add_field('walk', MessageField(field_number=4, required=True, message_cls=Time))
TimeToGo.add_field('jog', MessageField(field_number=5, required=True, message_cls=Time))
UnknownTimes.add_field('a', MessageField(field_number=1, required=True, message_cls=Time))
UnknownTimes.add_field('b', MessageField(field_number=2, required=True, message_cls=Time))
UnknownTimes.add_field('c', MessageField(field_number=3, required=True, message_cls=Time))
UnknownTimes.add_field('d', MessageField(field_number=4, required=True, message_cls=Time))
UnknownTimes.add_field('e', MessageField(field_number=5, required=True, message_cls=Time))
UnknownTimes.add_field('f', MessageField(field_number=6, required=True, message_cls=Time))
UnknownTimes.add_field('g', MessageField(field_number=7, required=True, message_cls=Time))
UnknownTimes.add_field('h', MessageField(field_number=8, required=True, message_cls=Time))

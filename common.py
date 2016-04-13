from protobuf3.fields import Int32Field, MessageField
from protobuf3.message import Message


class Date(Message):
    pass


class Time(Message):
    pass


class DateTime(Message):
    pass

Date.add_field('year', Int32Field(field_number=1, required=True))
Date.add_field('month', Int32Field(field_number=2, required=True))
Date.add_field('day', Int32Field(field_number=3, required=True))
Time.add_field('hours', Int32Field(field_number=1, required=True))
Time.add_field('minutes', Int32Field(field_number=2, required=True))
Time.add_field('seconds', Int32Field(field_number=3, required=True))
Time.add_field('milliseconds', Int32Field(field_number=4, required=True))
DateTime.add_field('date', MessageField(field_number=1, required=True, message_cls=Date))
DateTime.add_field('time', MessageField(field_number=2, required=True, message_cls=Time))

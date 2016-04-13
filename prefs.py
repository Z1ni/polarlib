from protobuf3.fields import Int32Field, MessageField
from protobuf3.message import Message
from common import DateTime


class Prefs(Message):
    pass


class Preferences(Message):
    pass

Prefs.add_field('prefs', MessageField(field_number=1, required=True, message_cls=Preferences))
Prefs.add_field('modified', MessageField(field_number=101, required=True, message_cls=DateTime))
Preferences.add_field('a', Int32Field(field_number=1, optional=True))
Preferences.add_field('b', Int32Field(field_number=2, optional=True))
Preferences.add_field('c', Int32Field(field_number=3, optional=True))
Preferences.add_field('d', Int32Field(field_number=4, optional=True))
Preferences.add_field('e', Int32Field(field_number=5, optional=True))
Preferences.add_field('f', Int32Field(field_number=6, optional=True))
Preferences.add_field('g', Int32Field(field_number=7, optional=True))
Preferences.add_field('h', Int32Field(field_number=8, optional=True))

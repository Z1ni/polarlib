from protobuf3.fields import Int32Field, MessageField, StringField
from protobuf3.message import Message


class DeviceInfo(Message):
    pass


class Version(Message):
    pass

DeviceInfo.add_field('bootloaderVer', MessageField(field_number=1, required=True, message_cls=Version))
DeviceInfo.add_field('platformVer', MessageField(field_number=2, required=True, message_cls=Version))
DeviceInfo.add_field('deviceVer', MessageField(field_number=3, required=True, message_cls=Version))
DeviceInfo.add_field('svnRev', Int32Field(field_number=4, required=True))
DeviceInfo.add_field('devId', StringField(field_number=5, optional=True))
DeviceInfo.add_field('serial', StringField(field_number=6, required=True))
DeviceInfo.add_field('model', StringField(field_number=7, required=True))
DeviceInfo.add_field('hwCode', StringField(field_number=8, required=True))
DeviceInfo.add_field('color', StringField(field_number=9, required=True))
DeviceInfo.add_field('design', StringField(field_number=10, required=True))
DeviceInfo.add_field('sysId', StringField(field_number=11, required=True))
Version.add_field('major', Int32Field(field_number=1, required=True))
Version.add_field('minor', Int32Field(field_number=2, required=True))
Version.add_field('patch', Int32Field(field_number=3, required=True))

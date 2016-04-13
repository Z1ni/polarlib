from protobuf3.fields import EnumField, FloatField, Int32Field, MessageField
from protobuf3.message import Message
from common import Date, DateTime
from enum import Enum


class PhysicalInformation(Message):
    pass


class Birthday(Message):
    pass


class Gender(Message):
    pass


class Weight(Message):
    pass


class Height(Message):
    pass


class VO2Max(Message):
    pass


class TrainingBackground(Message):
    pass


class GenderOption(Enum):
    MALE = 1
    FEMALE = 2


class TrainingBackgroundOption(Enum):
    OCCASIONAL = 10

PhysicalInformation.add_field('birthday', MessageField(field_number=1, required=True, message_cls=Birthday))
PhysicalInformation.add_field('gender', MessageField(field_number=2, required=True, message_cls=Gender))
PhysicalInformation.add_field('weight', MessageField(field_number=3, required=True, message_cls=Weight))
PhysicalInformation.add_field('height', MessageField(field_number=4, required=True, message_cls=Height))
PhysicalInformation.add_field('vo2max', MessageField(field_number=10, optional=True, message_cls=VO2Max))
PhysicalInformation.add_field('trainingBackground', MessageField(field_number=11, optional=True, message_cls=TrainingBackground))
PhysicalInformation.add_field('modified', MessageField(field_number=100, required=True, message_cls=DateTime))
Birthday.add_field('value', MessageField(field_number=1, required=True, message_cls=Date))
Birthday.add_field('modified', MessageField(field_number=2, required=True, message_cls=DateTime))
Gender.add_field('value', EnumField(field_number=1, required=True, enum_cls=GenderOption))
Gender.add_field('modified', MessageField(field_number=2, required=True, message_cls=DateTime))
Weight.add_field('value', FloatField(field_number=1, required=True))
Weight.add_field('modified', MessageField(field_number=2, required=True, message_cls=DateTime))
Height.add_field('value', FloatField(field_number=1, required=True))
Height.add_field('modified', MessageField(field_number=2, required=True, message_cls=DateTime))
VO2Max.add_field('value', Int32Field(field_number=1, required=True))
VO2Max.add_field('modified', MessageField(field_number=2, required=True, message_cls=DateTime))
TrainingBackground.add_field('value', EnumField(field_number=1, required=True, enum_cls=TrainingBackgroundOption))
TrainingBackground.add_field('modified', MessageField(field_number=2, required=True, message_cls=DateTime))

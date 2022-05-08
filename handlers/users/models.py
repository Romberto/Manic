from peewee import *

db = SqliteDatabase('data/timetable.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    chat_id = IntegerField()
    first_name = CharField(null=True)
    last_name = CharField(null=True)


class TimeTable(BaseModel):
    day = DateField()
    time_zone = CharField()
    free = BooleanField(default=True)
    name = CharField(null=True)
    chat_id = CharField(null=True)

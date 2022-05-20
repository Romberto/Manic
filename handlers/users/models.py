from peewee import *

db = SqliteDatabase('data/timetable.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    chat_id = IntegerField()
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    phone = CharField(null=True)
    is_active = BooleanField(default=False)


class TimeTable(BaseModel):
    day = DateField()
    time_zone = CharField()
    free = BooleanField(default=True)


class RecordRegistration(BaseModel):
    service = CharField()
    cunsomer_user = ForeignKeyField(Users, on_delete='CASCADE', related_name='users')
    time_table = ForeignKeyField(TimeTable, on_delete='CASCADE', related_name='records')



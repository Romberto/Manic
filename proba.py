from handlers.users.models import TimeTable, Users, RecordRegistration
from handlers.users.manager import TimeManager, data_str, str_to_date
from datetime import datetime
import datetime
import calendar

def date_to_str(date):
    date_str = datetime.datetime.strftime(date,'%d.%m')
    return date_str


def set_date():
    _day = data_str('19.05')
    query = TimeTable.select().where(TimeTable.day == _day, TimeTable.free == False)
    if query:
        print('есть')
    else:
        print('no')




if __name__ == '__main__':
    set_date()

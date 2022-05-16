from data.config import SERVISES
from handlers.users.models import TimeTable, Users, RecordRegistration
from handlers.users.manager import TimeManager, data_str, str_to_date
from datetime import datetime
import datetime
import calendar

def date_to_str(date):
    date_str = datetime.datetime.strftime(date,'%d.%m')
    return date_str


def set_date():
    for key, text in SERVISES.items():
        print(key, text)






if __name__ == '__main__':
    set_date()

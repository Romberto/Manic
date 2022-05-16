from data.config import SERVISES
from handlers.users.models import TimeTable, Users, RecordRegistration
from handlers.users.manager import TimeManager, data_str, str_to_date
from datetime import datetime
import datetime
import calendar
from fpdf import FPDF


def date_to_str(date):
    date_str = datetime.datetime.strftime(date, '%d.%m')
    return date_str


def set_date(s):
    today = datetime.datetime.today().date()
    rr = TimeTable.select().order_by(TimeTable.day)
    for i in rr:
        if i.day > today:
            if i.records:
                for item in i.records:
                    print(i.day, i.time_zone, item.service)

        else:
            i.delete_instance()


if __name__ == '__main__':
    set_date('tomorrow')

import datetime
import calendar
from handlers.users.models import *


# преобразует строковую дату в datetime
def data(dates: str):
    year = datetime.datetime.now().year
    dates = str(year) + '.' + dates
    date = datetime.datetime.strptime(dates, '%Y.%d.%m')
    return date.date()


class TimeManager():
    def __init__(self, work_day: str):
        self.w_day = work_day

    def set_days(self):
        inter = ['08-10', '10-12', '12-14']  # временной интервал
        tt = TimeTable()
        tt.create_table(safe=True)
        print(self.w_day)
        date = data(self.w_day)
        query = TimeTable.select().where(TimeTable.day == date)
        if not query.exists():
            for interval in inter:
                tt.create(day=date, time_zone=interval)
        else:
            return True


# формирует список дат начиная с завтрашнего дня на заданое количество дней
async def day_list(quantity_days):
    today = datetime.datetime.today()
    day_list = []
    for day in range(1, quantity_days + 1):
        start = today + datetime.timedelta(days=day)
        days = start.date()
        day = str(days.day)
        if len(day) != 2:
            day = "0" + day
        month = str(days.month)
        if len(month) != 2:
            month = '0' + month
        date_str = day + '.' + month
        day_list.append(date_str)
    return day_list

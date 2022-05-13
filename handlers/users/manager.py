import datetime
import calendar

import peewee

from handlers.users.models import *


# преобразует строковую дату в datetime
def data_str(dates: str):
    year = datetime.datetime.now().year
    dates = str(year) + '.' + dates
    date = datetime.datetime.strptime(dates, '%Y.%d.%m')
    return date.date()


class TimeManager():
    def __init__(self):

        self.tt = TimeTable()

    def set_days(self, w_day: str):
        inter = ['10:00', '12:00', '14:00','16:00','18:00','20:00']  # временной интервал
        self.tt.create_table(safe=True)
        date = data_str(w_day)
        query = TimeTable.select().where(TimeTable.day == date)
        if not query.exists():
            for interval in inter:
                self.tt.create(day=date, time_zone=interval)
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


# забирает список рабочих дат из базы данных
async def get_days():
    today = datetime.datetime.today().date()
    work_days_list = []
    try:
        query = TimeTable.select(TimeTable.day).where(TimeTable.free == True, TimeTable.day > today).distinct()
        for i in query:
            date = i.day
            str_day = datetime.datetime.strftime(date, '%d.%m')
            work_days_list.append(str_day)
        return work_days_list
    except peewee.OperationalError:
        return False


async def get_time(date: str):
    time_list = []
    year = datetime.datetime.today().year
    s_list = date.split('.')
    data = str(year) + '-' + s_list[0] + '-' + s_list[1]
    date_time_obj = datetime.datetime.strptime(data, '%Y-%d-%m')
    query = TimeTable.select().where(TimeTable.day == date_time_obj.date(), TimeTable.free == True)
    for i in query:
        time_list.append(i.time_zone)
    return time_list


# добавляет запись в базу данных

async def set_record(data: dict):
    d = data['date']
    service = data['service']
    d_obj = data_str(d)
    TimeTable.update({TimeTable.free: False}).where(TimeTable.day == d_obj,
                                                    TimeTable.time_zone == data['time']).execute()
    tt = TimeTable.select().where(TimeTable.day == d_obj, TimeTable.time_zone == data['time']).first()

    user = Users.select().where(Users.chat_id == 841163160).first()
    rr = RecordRegistration()
    rr.create_table(safe=True)

    query_rr = RecordRegistration.select().where(RecordRegistration.cunsomer_user == user,
                                                 RecordRegistration.service == service)
    if not query_rr.exists():
        rr.create(service=service,
                  cunsomer_user=user,
                  time_table=tt)

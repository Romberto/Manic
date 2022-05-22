import datetime
import calendar
import os

import peewee
from aiogram import types

from data.config import SERVISES
from handlers.users.models import *


# преобразует строковую дату в datetime
def data_str(dates: str):
    year = datetime.datetime.now().year
    dates = str(year) + '.' + dates
    date = datetime.datetime.strptime(dates, '%Y.%d.%m')
    return date.date()


async def date_to_str(date):
    date_str = datetime.datetime.strftime(date, '%d.%m')
    return date_str


async def str_to_date(dates: str):
    year = datetime.datetime.now().year
    dates = str(year) + '.' + dates
    date = datetime.datetime.strptime(dates, '%Y.%d.%m')
    return date.date()


class TimeManager():
    def __init__(self):
        self.tt = TimeTable()

    def set_days(self, w_day: str):
        inter = ['09:00', '12:00', '14:00', '16:00', '18:00']  # временной интервал
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
        query = TimeTable.select(TimeTable.day).where(TimeTable.free == True,
                                                      TimeTable.day >= today).distinct().order_by(TimeTable.day)
        for i in query:
            date = i.day
            str_day = datetime.datetime.strftime(date, '%d.%m')
            work_days_list.append(str_day)
        return work_days_list
    except peewee.OperationalError:
        return False


# возвращает список свободного времени
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

async def set_record(data: dict, chat_id):
    d = data['date']
    service = data['service']
    d_obj = data_str(d)

    tt = TimeTable.select().where(TimeTable.day == d_obj, TimeTable.time_zone == data['time']).first()
    TimeTable.update({TimeTable.free: False}).where(TimeTable.day == d_obj,
                                                    TimeTable.time_zone == data['time']).execute()
    user = Users.select().where(Users.chat_id == chat_id).first()
    rr = RecordRegistration()
    rr.create_table(safe=True)

    query_rr = RecordRegistration.select().where(RecordRegistration.cunsomer_user == user,
                                                 RecordRegistration.service == service)
    if not query_rr.exists():
        rr.create(service=SERVISES[service],
                  cunsomer_user=user,
                  time_table=tt,
                  confirm=False)


async def remove_pdf(dir_path):
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for file in filenames:
            if file.endswith('.pdf'):
                os.remove(dir_path + '/' + file)


async def validator_name(s):
    if not s.isalpha():
        return "Имя должно состоять только из букв"
    elif len(s) < 2:
        return "Имя не должно быть короче двух символов"
    else:
        return False


async def validator_name_l(s):
    if not s.isalpha():
        return "фамилия должна состоять только из букв"
    elif len(s) < 2:
        return "Фамилия не должна быть короче двух символов"
    else:
        return False


async def validator_phone(s):
    if s.startswith('+'):
        if not s[1:].isdigit():
            return "допустимые символы +(плюс) или цифры"
        elif len(s[1:]) != 11:
            return "номер либо слишком длинный , либо слишком короткий"
        else:
            return False
    else:
        if not s.isdigit():
            return "допустимые символы +(плюс) или цифры"
        elif len(s) != 11:
            return "номер либо слишком длинный , либо слишком короткий"
        else:
            return False


async def get_timetable_pdf(query, height, pdf):
    for item in query:
        if item.free == False:

            for i in item.records:
                pdf.set_text_color(255, 0, 0)
                row = (item.time_zone, i.service, i.cunsomer_user.first_name)
                for x, y in enumerate(row):
                    if x == 0:
                        pdf.set_font("FreeSansBo", style='B', size=18)
                        pdf.set_text_color(255, 0, 0)
                        pdf.cell(20, height, y, 0, 0, 'J')
                        pdf.set_font("FreeSans", size=20)
                    elif x == 1:
                        pdf.set_text_color(0, 128, 0)
                        pdf.cell(100, height, y, 0, 0, 'J')
                    elif x == 2:
                        pdf.set_text_color(0, 0, 10)
                        pdf.cell(20, height, y, 0, 1, 'J')

        else:
            row = (item.time_zone, 'свободно')
            for x, y in enumerate(row):
                if x == 0:
                    pdf.set_font("FreeSansBo", style='B', size=18)
                    pdf.set_text_color(255, 0, 0)
                    pdf.cell(20, height, y, 0, 0, 'J')
                    pdf.set_font("FreeSans", size=20)

                elif x == 1:
                    pdf.set_text_color(0, 0, 10)
                    pdf.cell(100, height, y, 0, 1, 'J')

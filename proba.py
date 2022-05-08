from handlers.users.models import TimeTable
from handlers.users.manager import TimeManager
from datetime import datetime
import datetime
import calendar


def main(s: str):
    time_list = []
    year = datetime.datetime.today().year
    s_list = s.split('.')
    data = str(year) + '-' + s_list[0] + '-' + s_list[1]
    date_time_obj = datetime.datetime.strptime(data, '%Y-%d-%m')
    query = TimeTable.select().where(TimeTable.day == date_time_obj.date(), TimeTable.free == True)
    for i in query:
        time_list.append(i.time_zone)
    return time_list


if __name__ == '__main__':
    main('13.05')

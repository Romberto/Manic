import datetime
from time import sleep

from handlers.users.models import TimeTable



def main():
    today = datetime.datetime.today().date()
    check_date = today + datetime.timedelta(days=1)
    query = TimeTable.select().where(TimeTable.day == check_date)
    for item in query:
        for record  in item.records:
            chat_id = record.cunsomer_user.chat_id

            print(chat_id, item.time_zone)






if __name__ == '__main__':
    main()

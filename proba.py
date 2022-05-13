from handlers.users.models import TimeTable, Users, RecordRegistration
from handlers.users.manager import TimeManager, data_str
from datetime import datetime
import datetime
import calendar


def set_date(data: dict):
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


if __name__ == '__main__':
    data = {'date': '16.05', 'time': '12:00', 'service': 'pediqur'}
    main(data)

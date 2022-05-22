import datetime
from time import sleep

from handlers.users.models import TimeTable, RecordRegistration, Users


def main():
    rr = RecordRegistration.select().where(RecordRegistration.confirm == False).first()
    user = rr.cunsomer_user
    if rr:

        tt = TimeTable.select().join(RecordRegistration).where(RecordRegistration.confirm == False, RecordRegistration.cunsomer_user == user).first()
        print(tt.day)





if __name__ == '__main__':
    main()

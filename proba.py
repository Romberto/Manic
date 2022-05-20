import datetime
from time import sleep

from handlers.users.models import TimeTable, RecordRegistration, Users


def main():
    user = Users.select(Users.id).where(Users.chat_id == 841163160).first()
    query = RecordRegistration.select().where(RecordRegistration.cunsomer_user == user).first()
    print(query.service)







if __name__ == '__main__':
    main()

from handlers.users.manager import date_to_str
from handlers.users.models import TimeTable, Users, RecordRegistration
from loader import dp
from aiogram import types


@dp.callback_query_handler()
async def confim_record(call: types.CallbackQuery):
    if call.data:
        data_list = call.data.split(' ')
        user = int(data_list[0])
        date = data_list[1]
        time = data_list[2]
        rr = RecordRegistration.select().where(RecordRegistration.confirm == False).first()
        if rr:
            rr.confirm = True
            rr.save()
        await call.message.answer("вы подтвердили запись, клиенту отправленно сообщение")
        await dp.bot.send_message(chat_id=call.message.chat.id, text=f'Мастер подтвердил запись, и ждёт вас {date} {time}')


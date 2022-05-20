from handlers.users.manager import date_to_str
from handlers.users.models import Users, RecordRegistration
from loader import dp
from aiogram import types


@dp.message_handler(content_types=types.ContentType.TEXT, text='моя запись')
async def my_record(message: types.Message):
    user = Users.select().where(Users.chat_id == 841163160).first()
    if user.is_active:
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('записаться'),
             types.KeyboardButton('моя запись')],
        ], resize_keyboard=True, one_time_keyboard=True)
        query = RecordRegistration.select().where(RecordRegistration.cunsomer_user == user).first()
        if query:
            date = await date_to_str(query.time_table.day)
            service = query.service
            time = query.time_table.time_zone
            text_message = f'* {date} вы записаны на {service}, ' \
                              f'мастер ждёт вас в {time} *'
            await message.answer(text_message, reply_markup=start)

        else:

            await message.answer('Вы ещё не записаны, записаться ?', reply_markup=start)
    else:
        kb_reg = types.ReplyKeyboardMarkup([
            [
                types.KeyboardButton('зарегистрироваться')
            ]
        ], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Пройдите регистрацию, чтобы мастер имел возможность связаться с вами',
                             reply_markup=kb_reg)

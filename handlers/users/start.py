from handlers.users.models import Users
from loader import dp
from aiogram import types

from state.states import WorkTimeTable


@dp.message_handler(commands='start')
async def start(message: types.Message):
    user = Users()
    user.create_table(safe=True)
    user.create(chat_id=message.chat.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name)
    start = types.ReplyKeyboardMarkup([
        [types.KeyboardButton('записаться')],
    ], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f'Привет {message.from_user.first_name}', reply_markup=start)



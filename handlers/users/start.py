from aiogram.dispatcher import FSMContext

from handlers.users.models import Users
from loader import dp
from aiogram import types

@dp.message_handler(commands='start')
async def start(message: types.Message):
    user = Users()
    user.create_table(safe=True)
    if message.from_user.first_name:
        first_name = message.from_user.first_name
    else:
        first_name = None
    if message.from_user.last_name:
        last_name = message.from_user.last_name
    else:
        last_name = None
    query = Users.select().where(Users.chat_id == message.chat.id)
    if not query.exists():
        user.create(chat_id=message.chat.id,
                    first_name=first_name,
                    last_name=last_name)
    for item in query:
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('зарегистрироваться')],
        ], resize_keyboard=True, one_time_keyboard=True)
        if item.is_active == True:
            start = types.ReplyKeyboardMarkup([
                [types.KeyboardButton('записаться')],
            ], resize_keyboard=True, one_time_keyboard=True)

    await message.answer(f'Привет {message.from_user.first_name}', reply_markup=start)


@dp.message_handler(state='*', text='/start')
async def start_tetx(message:types.Message, state: FSMContext):
    await state.finish()
    user = Users()
    user.create_table(safe=True)
    if message.from_user.first_name:
        first_name = message.from_user.first_name
    else:
        first_name = None
    if message.from_user.last_name:
        last_name = message.from_user.last_name
    else:
        last_name = None
    query = Users.select().where(Users.chat_id == message.chat.id).first()
    if not query:
        user.create(chat_id=message.chat.id,
                    first_name=first_name,
                    last_name=last_name)
    if query.is_active == True:
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('записаться')],
        ], resize_keyboard=True, one_time_keyboard=True)
    else:
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('зарегистрироваться')],
        ], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(f'Привет {message.from_user.first_name}', reply_markup=start)
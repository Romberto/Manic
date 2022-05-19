from aiogram.dispatcher import FSMContext

from data.config import is_admins
from handlers.users.models import Users
from keyboard.nav import kb_table_menu
from state.states import WorkTimeTable
from loader import dp
from aiogram import types
from handlers.users.manager import TimeManager, day_list

@dp.message_handler(commands='timetable', state='*')
async def table_menu(message:types.Message):
    if message.chat.id in is_admins:

        await WorkTimeTable.table_work.set()
        await message.answer('Работа с графиком', reply_markup=kb_table_menu)
    else:
        user = Users.select().where(Users.chat_id == message.chat.id).first()
        if user.is_active == True:
            start = types.ReplyKeyboardMarkup([
                [types.KeyboardButton('записаться')],
            ], resize_keyboard=True, one_time_keyboard=True)
        else:
            start = types.ReplyKeyboardMarkup([
                [types.KeyboardButton('зарегистрироваться')],
            ], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('у вас нет прав , для работы с графиком', reply_markup=start)







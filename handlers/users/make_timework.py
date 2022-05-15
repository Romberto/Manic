from aiogram.dispatcher import FSMContext

from keyboard.nav import kb_table_menu
from state.states import WorkTimeTable
from loader import dp
from aiogram import types
from handlers.users.manager import TimeManager, day_list

@dp.message_handler(commands='timetable', state='*')
async def table_menu(message:types.Message):
    await WorkTimeTable.table_work.set()
    await message.answer('Работа с графиком', reply_markup=kb_table_menu)







from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.manager import get_days, get_time
from handlers.users.models import TimeTable
from keyboard.nav import kb_table_menu
from loader import dp
from proba import date_to_str
from state.states import WorkTimeTable
from data.config import SERVISES


@dp.message_handler(text='Добавить запись', state=WorkTimeTable.table_work)
async def edit_record(message:types.Message, state: FSMContext):
    query_date = await get_days()
    kb_remove_record = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for item in query_date:
        buttons.append(types.InlineKeyboardButton(text=item, callback_data=item))
    buttons.append(types.InlineKeyboardButton(text='назад', callback_data='end'))
    kb_remove_record.add(*buttons)
    await WorkTimeTable.tw_edit_date.set()
    await message.answer('выберите дату:', reply_markup=kb_remove_record)

@dp.callback_query_handler(state=WorkTimeTable.tw_edit_date)
async def edit_cb_record(call:types.CallbackQuery, state:FSMContext):
    if call.data == 'end':
        await WorkTimeTable.table_work.set()
        await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
    else:
        date = call.data
        await state.update_data(date=call.data)  # запись даты в state
        time = await get_time(date)
        kb_time = types.InlineKeyboardMarkup(row_width=4)
        buttons = []
        for time_zone in time:
            buttons.append(types.InlineKeyboardButton(text=time_zone, callback_data=time_zone))
        buttons.append(types.InlineKeyboardButton(text='назад', callback_data='end'))
        kb_time.add(*buttons)
        await call.message.answer('выберите свободное время', reply_markup=kb_time)
        await WorkTimeTable.tw_edit_time.set()

@dp.callback_query_handler(state=WorkTimeTable.tw_edit_time)
async def edit_cb_time(call:types.CallbackQuery):
    if call.data == 'end':
        await WorkTimeTable.table_work.set()
        await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
    else:
        kb_edit = types.InlineKeyboardMarkup(row_width=1)
        buttons = []
        for key, text in SERVISES.items():
            buttons.append(types.InlineKeyboardButton(text=text, callback_data=key))
        buttons.append(types.InlineKeyboardButton(text='назад', callback_data='end'))
        kb_edit.add(*buttons)
        await call.message.answer('выберите услугу', reply_markup=kb_edit)
        await WorkTimeTable.tw_edit_servise.set()






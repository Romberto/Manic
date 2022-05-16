import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.manager import date_to_str, str_to_date
from handlers.users.models import TimeTable
from keyboard.nav import kb_table_menu
from loader import dp
from state.states import WorkTimeTable


# удалить дату из графика

@dp.message_handler(text='Удалить дату', state=WorkTimeTable.table_work)
async def remove_date(message: types.Message):
    today = datetime.datetime.today().date()
    query_date = TimeTable.select(TimeTable.day).where(TimeTable.day > today).distinct().order_by(TimeTable.day)
    kb_remove_day = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for day in query_date:
        _day = await date_to_str(day.day)
        buttons.append(types.InlineKeyboardButton(text=_day, callback_data=_day))
    buttons.append(types.InlineKeyboardButton(text='назад', callback_data='end'))
    kb_remove_day.add(*buttons)
    await WorkTimeTable.tw_remove_day.set()
    await message.answer('выберите дату для удаления из графика', reply_markup=kb_remove_day)


@dp.callback_query_handler(state=WorkTimeTable.tw_remove_day)
async def cb_remove_date(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'end':
        await WorkTimeTable.table_work.set()
        await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
    else:
        date = call.data
        _day = await str_to_date(date)
        # проверка , есть ли записи на удаляемую дату
        query = TimeTable.select().where(TimeTable.day == _day, TimeTable.free == False)
        if query:
            await state.update_data(data_obj=call.data)
            await WorkTimeTable.tw_remove_day_cb.set()
            kb_table_cb_menu = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton(text='да', callback_data='yes'),
                types.InlineKeyboardButton(text='нет', callback_data='no')
            ]
            kb_table_cb_menu.add(*buttons)
            await call.message.answer(f'На {call.data} есть записи,\n вы действительно хотите удалить дату ?',
                                      reply_markup=kb_table_cb_menu)
        else:
            TimeTable.delete().where(TimeTable.day == _day).execute()
            await WorkTimeTable.table_work.set()
            await call.message.answer(f'дата {date} удалена из графика', reply_markup=kb_table_menu)


@dp.callback_query_handler(state=WorkTimeTable.tw_remove_day_cb)
async def call_remove_date(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        d = await state.get_data()
        date = d['data_obj']
        _day = await str_to_date(date)
        TimeTable.delete().where(TimeTable.day == _day).execute()
        await WorkTimeTable.table_work.set()
        await call.message.answer(f'дата {date} удалена из графика', reply_markup=kb_table_menu)
    elif call.data == 'no':
        await WorkTimeTable.table_work.set()
        await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)

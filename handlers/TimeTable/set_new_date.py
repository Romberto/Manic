from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.manager import day_list, TimeManager
from keyboard.nav import kb_table_menu
from loader import dp
from state.states import WorkTimeTable


@dp.message_handler(text='Добавить новые даты', state=WorkTimeTable.table_work)
async def work_days(message: types.Message, state: FSMContext):
    await WorkTimeTable.choice_dates.set()
    kb_table_days = types.InlineKeyboardMarkup(row_width=5)
    buttons_day = []
    """ устанавливаем количество дней """
    _range = await day_list(21)
    await state.update_data(_range=_range)
    for day in _range:

        buttons_day.append(types.InlineKeyboardButton(text=day, callback_data=day))
    buttons_day.append(types.InlineKeyboardButton(text='готово', callback_data='end'))
    kb_table_days.add(*buttons_day)
    await message.answer('укажите рабочие дни  \n',
                         reply_markup=kb_table_days)


@dp.callback_query_handler(state=WorkTimeTable.choice_dates)
async def set_day(call:types.CallbackQuery, state:FSMContext,):
    if call.data == 'end':
        await WorkTimeTable.table_work.set()
        await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
    else:
        tm = TimeManager()
        exists = tm.set_days(call.data)
        if not exists:
            data = await state.get_data()
            _range = data['_range']
            _range.remove(call.data)
            await state.update_data(_range=_range)
            kb_table_days = types.InlineKeyboardMarkup(row_width=4)
            buttons_day = []
            for day in _range:
                buttons_day.append(types.InlineKeyboardButton(text=day, callback_data=day))
            buttons_day.append(types.InlineKeyboardButton(text='готово', callback_data='end'))
            kb_table_days.add(*buttons_day)

            await call.message.answer(f'дата {call.data} установленна в график', reply_markup=kb_table_days)
            return
        else:
            await call.message.answer(f' {call.data} дата уже есть в графике')
            return

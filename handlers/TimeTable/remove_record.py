from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.manager import date_to_str, str_to_date
from handlers.users.models import TimeTable, RecordRegistration
from keyboard.nav import kb_table_menu
from loader import dp
from state.states import WorkTimeTable


@dp.message_handler(text='Удалить запись', state=WorkTimeTable.table_work)
async def remove_record(message: types.Message, state: FSMContext):
    query_date = TimeTable.select(TimeTable.day).where(TimeTable.free == False).distinct().order_by(TimeTable.day)
    kb_remove_record = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for item in query_date:
        _day = await date_to_str(item.day)
        buttons.append(types.InlineKeyboardButton(text=_day, callback_data=_day))
    buttons.append(types.InlineKeyboardButton(text='назад', callback_data='end'))
    kb_remove_record.add(*buttons)
    await message.answer('УДАЛИТЬ ЗАПИСЬ\n'
                         'выберите дату', reply_markup=kb_remove_record)
    await WorkTimeTable.tw_remove_record.set()


@dp.callback_query_handler(state=WorkTimeTable.tw_remove_record)
async def cb_remove_record(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'end':
        await WorkTimeTable.table_work.set()
        await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
    else:
        await state.update_data(day=call.data)
        date = await str_to_date(call.data)
        query = TimeTable.select(TimeTable.time_zone).where(TimeTable.day == date, TimeTable.free == False)
        kb_remove_records = types.InlineKeyboardMarkup(row_width=5)
        buttons = []
        for item in query:
            text = item.time_zone
            buttons.append(types.InlineKeyboardButton(text=item.time_zone, callback_data=item.time_zone))
        buttons.append(types.InlineKeyboardButton(text="назад", callback_data='end'))
        kb_remove_records.add(*buttons)
        await WorkTimeTable.tw_remove_record_cb.set()
        await call.message.answer('УДАЛИТЬ ЗАПИСЬ\n'
                                  'выберите запись', reply_markup=kb_remove_records)


@dp.callback_query_handler(state=WorkTimeTable.tw_remove_record_cb)
async def cb_remove_time(call: types.CallbackQuery, state: FSMContext):
    cb = call.data
    if cb == 'end':
        await WorkTimeTable.table_work.set()
        await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
    else:
        d = await state.get_data()
        date = await str_to_date(d['day'])
        await state.update_data(time=call.data)
        tt = TimeTable.select(TimeTable.id).where(TimeTable.day == date, TimeTable.time_zone == cb).first()
        tt.free = True
        tt.save()
        rr = RecordRegistration.select().where(RecordRegistration.time_table == tt).first()
        user_chat_id = rr.cunsomer_user.chat_id
        data_d = rr.time_table.day
        data_t = rr.time_table.time_zone
        data_s = rr.service
        data_fn = rr.cunsomer_user.first_name
        await call.message.answer(f'запись на \n'
                                  f'дата {data_d} \n'
                                  f'время{data_t}\n'
                                  f'{data_s} \n'
                                  f'ОТМЕНЕНА \n')
        rr.delete_instance()
        await dp.bot.send_message(chat_id=user_chat_id, text=f'{data_fn} ваша запись на {data_s} \n'
                                                             f'отменина')
        await WorkTimeTable.table_work.set()
        #todo отправить сообщение пользователю, о том что его запись отменина




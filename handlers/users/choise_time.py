from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.manager import get_time
from loader import dp
from state.states import ServisChoise

@dp.callback_query_handler(state=ServisChoise.choise_date)
async def choise_time(call:types.CallbackQuery, state:FSMContext):
    date = call.data
    await state.update_data(date=call.data) # запись даты в state
    time = await get_time(date)
    kb_time = types.InlineKeyboardMarkup(row_width=4)
    buttons = []
    for time_zone in time:
        buttons.append(types.InlineKeyboardButton(text=time_zone, callback_data=time_zone))
    kb_time.add(*buttons)
    await call.message.answer('выберите свободное время',reply_markup=kb_time)
    await ServisChoise.choise_time.set()

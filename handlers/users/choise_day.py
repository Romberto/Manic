from datetime import date, timedelta

from aiogram.dispatcher import FSMContext

from handlers.users.manager import TimeManager, get_days
from loader import dp

from aiogram import types

from state.states import ServisChoise


@dp.message_handler(content_types=types.ContentType.TEXT, text='записаться')
async def choise_date(message: types.Message, state: FSMContext):
    kb_enroll = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    day_list = await get_days()
    for day in day_list:
        buttons.append(types.InlineKeyboardButton(text=day, callback_data=day))
    kb_enroll.add(*buttons)
    await message.answer('это свободные даты , выбрайте', reply_markup=kb_enroll)
    await ServisChoise.choise_date.set()





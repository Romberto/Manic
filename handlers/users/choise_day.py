import datetime
from datetime import date, timedelta

from aiogram.dispatcher import FSMContext

from handlers.users.manager import TimeManager, get_days
from loader import dp

from aiogram import types

from state.states import ServisChoise
from handlers.users.models import TimeTable, Users


@dp.message_handler(content_types=types.ContentType.TEXT, text='записаться')
async def choise_date(message: types.Message, state: FSMContext):
    query = Users.select().where(Users.chat_id == message.chat.id).first()
    if query.is_active == True:
        kb_enroll = types.InlineKeyboardMarkup(row_width=5)
        buttons = []
        day_list = await get_days()
        if day_list:
            for day in day_list:
                buttons.append(types.InlineKeyboardButton(text=day, callback_data=day))
            kb_enroll.add(*buttons)
            await message.answer('это свободные даты , выбирайте', reply_markup=kb_enroll)
            await ServisChoise.choise_date.set()
        else:
            await message.answer('в графике нет дат')
            await state.finish()
    else:
        kb_reg = types.ReplyKeyboardMarkup([
            [
                types.KeyboardButton('зарегистрироваться')
            ]
        ],resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Проёдите регистрацию, чтобы мастер имел возможность связаться с вами', reply_markup=kb_reg)




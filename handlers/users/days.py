from datetime import date, timedelta

from loader import dp

from aiogram import types


@dp.message_handler(content_types=types.ContentType.TEXT, text='записаться')
async def enroll(message: types.Message):
    kb_enroll_calendar = types.InlineKeyboardMarkup(row_width=7)
    today = date.today()
    enroll_days = []
    for item in range(1, 15):
        day = today + timedelta(days=item)
        enroll_days.append(types.InlineKeyboardButton(text=f'{day.strftime("%d.%m")}',
                                                      callback_data=f'{day.strftime("%d.%m")}'))
    kb_enroll_calendar.add(*enroll_days)
    await message.answer('выберите дату', reply_markup=kb_enroll_calendar)

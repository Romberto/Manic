from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import SERVISES
from loader import dp
from state.states import ServisChoise

@dp.callback_query_handler(state=ServisChoise.choise_time)
async def choise_service(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(time=call.data) # записываем время в state
    kb_edit = types.InlineKeyboardMarkup(row_width=1)
    buttons = []
    for key, text in SERVISES.items():
        buttons.append(types.InlineKeyboardButton(text=text, callback_data=key))
    buttons.append(types.InlineKeyboardButton(text='назад', callback_data='end'))
    kb_edit.add(*buttons)
    await call.message.answer('выберите услугу', reply_markup=kb_edit)
    await ServisChoise.choise_servise.set()


from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from state.states import ServisChoise

@dp.callback_query_handler(state=ServisChoise.choise_time)
async def choise_service(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(time=call.data) # записываем время в state
    kb_servise = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text='ПЕДИКЮР', callback_data='pediqur'),
        types.InlineKeyboardButton(text='МАНИКЮР', callback_data='maniqur')
    ]
    kb_servise.add(*buttons)
    await call.message.answer('укажите услугу', reply_markup=kb_servise)
    await ServisChoise.choise_servise.set()


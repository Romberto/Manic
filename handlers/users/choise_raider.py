from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import price
from loader import dp
from state.states import ServisChoise
from keyboard.nav import prepayment

""" Выбор услуги """

@dp.callback_query_handler(state=ServisChoise.choise_servise)
async def choise_rider(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(service=call.data)  # записывыем вид услуги в state
    if call.data == 'pediqur':

        await call.message.answer('Вы выбрали услугу педикюр \n'
                                  f'стоимость {price["pediqur"]} руб \n'
                                  'предоплата 200 руб \n'
                                  '****\n'
                                  'перейти к предоплате?', reply_markup=prepayment)
        await ServisChoise.prepayment.set()
    elif call.data == 'maniqur':
        kb_manic = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text=f'с покрытием', callback_data="sp"),
            types.InlineKeyboardButton(text=f'без покрытия', callback_data='bp')
        ]
        kb_manic.add(*buttons)
        await ServisChoise.choise_manic.set()
        await call.message.answer('маникюр', reply_markup=kb_manic)

    @dp.message_handler(content_types=types.ContentType.TEXT, state=ServisChoise.choise_servise)
    async def text_error(message: types.Message, state: FSMContext):
        await message.answer('Пожалуйста используйте кнопки')

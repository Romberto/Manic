from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import price, SERVISES
from loader import dp
from state.states import ServisChoise, WorkTimeTable
from keyboard.nav import prepayment, kb_table_menu

""" Выбор услуги """


@dp.callback_query_handler(state=ServisChoise.choise_servise)
async def choise_rider(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    if call.data == 'end':
        await state.finish()
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('записаться')],
        ], resize_keyboard=True, one_time_keyboard=True)
        await call.message.answer('хотите записаться ?', reply_markup=start)
    else:
        prepayment = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text='предоплата', callback_data=call.data),
            types.InlineKeyboardButton(text='отмена', callback_data='cancel')
        ]
        prepayment.add(*buttons)
        text_message = f'Вы выбрали услугу {SERVISES[call.data]}\n'
        f'стоимость {price[call.data]} руб \n'
        'предоплата 200 руб \n'
        '****\n'
        'перейти к предоплате?'
        if call.data == 'manic_design':
            text_message =f'Вы выбрали услугу {SERVISES[call.data]}\n'\
        f'стоимость от {price[call.data]} руб \n'\
        'предоплата 200 руб \n'\
        f'ВНИМАНИЕ финальная стоимость услуги может измениться\n' \
        f'взависимости от сложности дизайна \n'\
        '****\n'\
        'перейти к предоплате?'
        await call.message.answer(text=text_message, reply_markup=prepayment)
        await state.update_data(service=call.data)
        await ServisChoise.prepayment.set()

    @dp.message_handler(content_types=types.ContentType.TEXT, state=ServisChoise.choise_servise)
    async def text_error(message: types.Message, ):
        await message.answer('Пожалуйста используйте кнопки')

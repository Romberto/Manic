from aiogram.dispatcher import FSMContext

from data.config import price
from loader import dp
from aiogram import types

from state.states import ServisChoise


@dp.callback_query_handler(state=ServisChoise.cover)
async def cover(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cover':# маникюр однотонный
        await state.update_data(service='manic_cover') # маникюр однотонный
        prepayment = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text='предоплата', callback_data='prepayment_cover'),
            types.InlineKeyboardButton(text='отмена', callback_data='cancel')
        ]
        prepayment.add(*buttons)
        await call.message.answer('Вы выбрали услугу маникюр с покрытием однотонный \n'
                                  f'стоимость {price["maniqur_no_disain"]} руб \n'
                                  'предоплата 200 руб \n'
                                  '****\n'
                                  'перейти к предоплате?', reply_markup=prepayment)
        await ServisChoise.prepayment.set()
    elif call.data == 'cover_ds':# маникюр с дизайном
        await state.update_data(service='manic_design') # маникюр с дизайном
        prepayment = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text='предоплата', callback_data='prepayment_cover_ds'),
            types.InlineKeyboardButton(text='отмена', callback_data='cancel')
        ]
        prepayment.add(*buttons)
        await call.message.answer('Вы выбрали услугу маникюр с дизайном \n'
                                  f'стоимость {price["maniqur_disain"]} руб \n'
                                  'предоплата 200 руб \n'
                                  '****\n'
                                  'перейти к предоплате?', reply_markup=prepayment)
        await ServisChoise.prepayment.set()




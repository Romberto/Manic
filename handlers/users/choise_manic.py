from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import price
from keyboard.nav import prepayment
from loader import dp
from state.states import ServisChoise


@dp.callback_query_handler(state=ServisChoise.choise_manic)
async def manic(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'sp':  # с покрытием
        await ServisChoise.cover.set()
        kb_cover = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text="однотонный", callback_data='cover'),
            types.InlineKeyboardButton(text="с дизайном", callback_data='cover_ds')
        ]
        kb_cover.add(*buttons)
        await call.message.answer('укажите тип покрытия', reply_markup=kb_cover)
    elif call.data == 'bp':  # без покрытия
        await state.update_data(service='manic_bp')
        prepayment = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton(text='предоплата', callback_data='pre_manic_bp'),
            InlineKeyboardButton(text='отмена', callback_data='cancel')
        ]
        prepayment.add(*buttons)
        await call.message.answer('Вы выбрали услугу маникюр без покрытия \n'
                                  f'стоимость {price["maniqur_no_pok"]} руб \n'
                                  'предоплата 200 руб \n'
                                  '****\n'
                                  'перейти к предоплате?', reply_markup=prepayment)
        await ServisChoise.prepayment.set()

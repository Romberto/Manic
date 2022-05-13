from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

prepayment = InlineKeyboardMarkup(row_width=2)
buttons = [
    InlineKeyboardButton(text='предоплата', callback_data='prepayment'),
    InlineKeyboardButton(text='отмена', callback_data='cancel')
]
prepayment.add(*buttons)

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

prepayment = InlineKeyboardMarkup(row_width=2)
buttons = [
    InlineKeyboardButton(text='предоплата', callback_data='prepayment'),
    InlineKeyboardButton(text='отмена', callback_data='cancel')
]
prepayment.add(*buttons)

kb_table_menu = ReplyKeyboardMarkup([
    [
        KeyboardButton('Добавить новые даты')
    ],
    [
        KeyboardButton('Удалить дату')
    ],
    [
        KeyboardButton('Добавить запись'),KeyboardButton('Удалить запись')
    ],
    [
        KeyboardButton('Посмотреть график'),KeyboardButton('Посмотреть записи')
    ]
], resize_keyboard=True, one_time_keyboard=True)

start = types.ReplyKeyboardMarkup([
    [types.KeyboardButton('записаться'),
     types.KeyboardButton('моя запись')],
], resize_keyboard=True, one_time_keyboard=True)
from aiogram.dispatcher import FSMContext

from data.config import MASTER
from handlers.users.manager import date_to_str
from handlers.users.models import Users, RecordRegistration
from keyboard.nav import start
from loader import dp
from aiogram import types

from state.states import MyRecordState


@dp.message_handler(content_types=types.ContentType.TEXT, text='моя запись')
async def my_record(message: types.Message):
    chat_id = message.chat.id
    user = Users.select().where(Users.chat_id == chat_id).first()
    if user.is_active:
        query = RecordRegistration.select().where(RecordRegistration.cunsomer_user == user).first()
        if query:
            date = await date_to_str(query.time_table.day)
            service = query.service
            time = query.time_table.time_zone
            text_message = f'* {date} вы записаны на {service}, ' \
                           f'мастер ждёт вас в {time} *'
            kb_my_rec = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton(text='отменить', callback_data='cancel'),
                types.InlineKeyboardButton(text='назад', callback_data='end')
            ]
            kb_my_rec.add(*buttons)
            await MyRecordState.mr_first.set()
            await message.answer(text_message, reply_markup=kb_my_rec)

        else:

            await message.answer('Вы ещё не записаны, записаться ?', reply_markup=start)
    else:
        kb_reg = types.ReplyKeyboardMarkup([
            [
                types.KeyboardButton('зарегистрироваться')
            ]
        ], resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Пройдите регистрацию, чтобы мастер имел возможность связаться с вами',
                             reply_markup=kb_reg)


@dp.callback_query_handler(state=MyRecordState.mr_first)
async def answer_me_rec(call: types.CallbackQuery, state: FSMContext):
    if call.data == "cancel":
        kb_cancel = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text='да', callback_data='yes'),
            types.InlineKeyboardButton(text='нет', callback_data='no')
        ]
        kb_cancel.add(*buttons)
        await MyRecordState.mr_second.set()
        await call.message.answer('Вы хотите отменить запись ?', reply_markup=kb_cancel)
    elif call.data == 'end':
        await state.finish()
        await call.message.answer('записаться ?', reply_markup=start)


@dp.callback_query_handler(state=MyRecordState.mr_second)
async def cancel_record(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        user = Users.select().where(Users.chat_id == call.message.chat.id).first()
        query = RecordRegistration.select().where(RecordRegistration.cunsomer_user == user).first()
        query.time_table.free = True
        date = await date_to_str(query.time_table.day)
        service = query.service
        time = query.time_table.time_zone
        text_message = f'* вы отменили запись на {service}, ' \
                       f'{date}  {time} *'
        query.time_table.save()
        query.delete_instance()
        await state.finish()
        await call.message.answer(text_message, reply_markup=start)
        await dp.bot.send_message(chat_id=MASTER, text=f'{user.first_name} {user.last_name} отменил запись\n'
                                                       f'на {service} {date} {time}')

    elif call.data == 'no':
        await state.finish()
        await call.message.answer('записаться ?', reply_markup=start)

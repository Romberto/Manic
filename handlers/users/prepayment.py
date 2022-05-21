from aiogram.dispatcher import FSMContext
from aiogram.types import LabeledPrice

from data.config import TEST_UKASSA, price, pred_price, SERVISES
from handlers.users.manager import data_str, set_record
from loader import dp
from loader import bot
from aiogram import types
from state.states import ServisChoise
from handlers.users.models import TimeTable, Users, RecordRegistration



@dp.callback_query_handler(state=ServisChoise.prepayment)
async def prepayment(call: types.CallbackQuery, state: FSMContext):
    PRICE = LabeledPrice(label='руб', amount=pred_price['pred_p'] * 100)
    if call.data == 'pediqur':
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_invoice(chat_id=call.message.chat.id,
                               title="pediqur",
                               description='Предоплата за педикюр',
                               payload='pediqur',
                               provider_token=TEST_UKASSA,
                               currency='RUB',
                               start_parameter='test_bot',
                               prices=[PRICE],
                               )
    elif call.data == 'manic_bp':
        await bot.send_invoice(chat_id=call.message.chat.id,
                               title="maniqur",
                               description='Предоплата за маникюр без покрытия',
                               payload='maniqur_bp',
                               provider_token=TEST_UKASSA,
                               currency='RUB',
                               start_parameter='test_bot',
                               prices=[PRICE],
                               )

    elif call.data == 'manic_cover':
        await bot.send_invoice(chat_id=call.message.chat.id,
                               title="maniqur_cover",
                               description='Предоплата за маникюр однотонный',
                               payload='maniqur_cover',
                               provider_token=TEST_UKASSA,
                               currency='RUB',
                               start_parameter='test_bot',
                               prices=[PRICE],
                               )
    elif call.data == 'manic_design':
        await bot.send_invoice(chat_id=call.message.chat.id,
                               title="maniqur_design",
                               description='Предоплата за маникюр с дизайном',
                               payload='maniqur_design',
                               provider_token=TEST_UKASSA,
                               currency='RUB',
                               start_parameter='test_bot',
                               prices=[PRICE],
                               )


    elif call.data == 'cancel':
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('записаться')],
        ], resize_keyboard=True, one_time_keyboard=True)
        await state.finish()
        await call.message.answer('начнём заново?', reply_markup=start)


@dp.pre_checkout_query_handler(state=ServisChoise.prepayment)
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)


# отправляем сообщение пльзователю в случае успешной оплаты
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state=ServisChoise.prepayment)
async def process_pay(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    d = state_data['date']
    t = state_data['time']
    await set_record(state_data, message.chat.id)
    user = Users.select().where(Users.chat_id == message.chat.id).first()
    if user.is_active == True:
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('записаться')],
        ], resize_keyboard=True, one_time_keyboard=True)
    else:
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('зарегистрироваться')],
        ], resize_keyboard=True, one_time_keyboard=True)
    await state.finish()
    if message.successful_payment.invoice_payload == 'pediqur':
        await message.answer(f''
                             f'Вы внесли предоплату \n'
                             f'и записаны на педикюр'
                             f'дата {d} \n'
                             f'время {t}', reply_markup=start)
    elif message.successful_payment.invoice_payload == 'maniqur_bp':
        await message.answer(f''
                             f'Вы внесли предоплату \n'
                             f'и записаны на маникюр без покрытия\n'
                             f'дата {d} \n'
                             f'время {t}', reply_markup=start)

    elif message.successful_payment.invoice_payload == 'maniqur_cover':
        await message.answer(f''
                             f'Вы внесли предоплату \n'
                             f'и записаны на маникюр однотонный\n'
                             f'дата {d} \n'
                             f'время {t}', reply_markup=start)

    elif message.successful_payment.invoice_payload == 'maniqur_design':
        await message.answer(f''
                             f'Вы внесли предоплату \n'
                             f'и записаны на маникюр с дизайном\n'
                             f'дата {d} \n'
                             f'время {t}', reply_markup=start)
    kb_confirm = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text='подтвердить', callback_data=f'{user} {d} {t}')]
    kb_confirm.add(*buttons)
    await dp.bot.send_message(chat_id=841163160, text='НОВАЯ ЗАПИСЬ \n'
                                                      f'Клиент {user.first_name} {user.last_name} '
                                                      f'внёс предоплату за '
                                                      f'{SERVISES[state_data["service"]]}\n'
                                                      f'на {d} {t}', reply_markup=kb_confirm)

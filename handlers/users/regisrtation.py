from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.manager import validator_name, validator_name_l, validator_phone
from handlers.users.models import Users
from loader import dp
from state.states import RegistrationState


@dp.message_handler(content_types=types.ContentType.TEXT, text='зарегистрироваться')
async def choise_date(message: types.Message, state: FSMContext):
    user = Users.select().where(Users.chat_id == message.chat.id).first()
    if user.first_name:
        await state.update_data(first_name=user.first_name)
        await message.answer('Здорово ваше имя мне известно, отправте вашу фамилию')
        await RegistrationState.reg_step_name.set()
    elif user.first_name and user.last_name:
        await state.update_data(first_name=user.first_name, last_name=user.last_name)
        await message.answer('Отлично ,укажите свой телефон (пример +79992223311 или 89993332211')
        await RegistrationState.reg_step_phone.set()
    else:
        await RegistrationState.reg_step_first.set()
        await message.answer('Ок, отправте мне своё имя')


@dp.message_handler(content_types=types.ContentType.TEXT, state=RegistrationState.reg_step_first)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    err_validator = await validator_name(name)
    if err_validator:
        await message.answer(err_validator)
        return
    else:
        await state.update_data(first_name=name)
        await message.answer('Хорошо, отправте вашу фамилию')
        await RegistrationState.reg_step_name.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=RegistrationState.reg_step_name)
async def get_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    err_validator = await validator_name_l(last_name)
    if err_validator:
        await message.answer(err_validator)
        return
    else:
        await state.update_data(last_name=last_name)
        await message.answer('Отлично ,укажите свой телефон (пример +79992223311 или 89993332211')
        await RegistrationState.reg_step_phone.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=RegistrationState.reg_step_phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text
    arr_validator_phone = await validator_phone(phone)
    if arr_validator_phone:
        await message.answer(arr_validator_phone)
        return
    else:
        state_data = await state.get_data()
        first_name = state_data['first_name']
        last_name = state_data['last_name']
        phone = message.text
        Users.update({Users.first_name: first_name, Users.last_name: last_name,
                             Users.phone: phone, Users.is_active: True}).where(
            Users.chat_id == message.chat.id).execute()
        await state.finish()
        start = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('записаться')],
        ], resize_keyboard=True, one_time_keyboard=True)
        await message.answer(f'Чудесно {first_name} Регистрация завершена', reply_markup=start)

from aiogram import types , Dispatcher

async  def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('/timetable', 'работа с расписанием'),
        types.BotCommand('/start', 'Старт')
    ]
    )

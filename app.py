import logging


async def on_startup(dp):
    from utils.set_bot_commands import set_commands
    await set_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, on_startup=on_startup)

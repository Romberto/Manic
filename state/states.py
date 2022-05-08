from aiogram.dispatcher.filters.state import StatesGroup, State


class WorkTimeTable(StatesGroup):
    choice_dates = State()

class ServisChoise(StatesGroup):
    choise_date = State()
    choise_time =State()

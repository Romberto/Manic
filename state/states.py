from aiogram.dispatcher.filters.state import StatesGroup, State


class WorkTimeTable(StatesGroup):
    choice_dates = State()

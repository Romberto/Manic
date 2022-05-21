from aiogram.dispatcher.filters.state import StatesGroup, State


class WorkTimeTable(StatesGroup):
    table_work = State()
    tw_view_tomorrow = State()
    tw_view_record = State()
    tw_remove_day = State()
    tw_remove_day_cb = State()
    tw_remove_record = State()
    tw_remove_record_cb = State()
    tw_edit_date = State()
    tw_edit_time = State()
    tw_edit_servise = State()
    choice_dates = State()


class ServisChoise(StatesGroup):
    choise_date = State()
    choise_time = State()
    choise_servise = State()
    shoise_rider = State()
    choise_manic = State()
    cover = State()
    prepayment = State()


class RegistrationState(StatesGroup):
    reg_step_first = State()
    reg_step_name = State()
    reg_step_phone = State()


class MyRecordState(StatesGroup):
    mr_first = State()
    mr_second = State()

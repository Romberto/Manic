import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from fpdf import FPDF

from handlers.users.manager import remove_pdf, get_timetable_pdf
from handlers.users.models import TimeTable
from keyboard.nav import kb_table_menu
from loader import dp
from state.states import WorkTimeTable


@dp.message_handler(text='Посмотреть график', state=WorkTimeTable.table_work)
async def view_chart(message: types.Message):
    kb_chart = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text='График на сегодня', callback_data="today"),
        types.InlineKeyboardButton(text='График на завтра', callback_data="tomorrow"),
        types.InlineKeyboardButton(text='График на неделю', callback_data="week"),
        types.InlineKeyboardButton(text='График', callback_data="totally")
    ]
    kb_chart.add(*buttons)
    await WorkTimeTable.tw_view_tomorrow.set()
    await message.answer('Выберите график', reply_markup=kb_chart)


@dp.callback_query_handler(state=WorkTimeTable.tw_view_tomorrow)
async def view_cb_chart(call: types.CallbackQuery, state: FSMContext):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font('FreeSans', '', r'fonts/FreeSans.ttf', uni=True)
    pdf.add_font('FreeSansBo', 'B', r'fonts/FreeSansBold.ttf', uni=True)
    height = 12
    if call.data == 'tomorrow':
        pdf.set_font("FreeSans", size=20)
        pdf.set_text_color(255, 0, 0)
        tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
        date_str = datetime.datetime.strftime(tomorrow, '%d.%m')
        text = f'График на {date_str}'
        pdf.cell(100, 20, text, 0, 1, 'L')
        query = TimeTable.select().where(TimeTable.day == tomorrow)
        await get_timetable_pdf(query=query, height=height, pdf=pdf)
    elif call.data == 'today':
        pdf.set_font("FreeSans", size=20)
        pdf.set_text_color(255, 0, 0)
        today= (datetime.datetime.today()).date()
        date_str = datetime.datetime.strftime(today, '%d.%m')
        text = f'График на {date_str}'
        pdf.cell(100, 20, text, 0, 1, 'L')
        query = TimeTable.select().where(TimeTable.day == today)
        if query:
            await get_timetable_pdf(query=query, height=height, pdf=pdf)
        else:
            await call.message.answer('на сегодня записей нет')
            return

    elif call.data == 'week':
        for day in range(0, 8):
            pdf.set_font("FreeSans", size=20)
            pdf.set_text_color(255, 0, 0)
            d = (datetime.datetime.today() + datetime.timedelta(days=day)).date()
            date_str = datetime.datetime.strftime(d, '%d.%m')
            text = f'График на {date_str}'
            pdf.cell(100, 20, text, 0, 1, 'L')
            query = TimeTable.select().where(TimeTable.day == d)
            if query:
                await get_timetable_pdf(query=query, height=height, pdf=pdf)
            else:
                pdf.set_text_color(0, 128, 0)
                pdf.cell(100, height, 'ВЫХОДНОЙ', 0, 1, 'J')
                pdf.set_text_color(0, 0, 10)
            pdf.set_text_color(0, 128, 0)
            pdf.cell(100, height, '*-' * 20, 0, 1, 'J')
            pdf.set_text_color(0, 0, 10)

    elif call.data == 'totally':
        for day in range(0, 22):
            pdf.set_font("FreeSans", size=20)
            pdf.set_text_color(255, 0, 0)
            d = (datetime.datetime.today() + datetime.timedelta(days=day)).date()
            date_str = datetime.datetime.strftime(d, '%d.%m')
            text = f'График на {date_str}'
            pdf.cell(100, 20, text, 0, 1, 'L')
            query = TimeTable.select().where(TimeTable.day == d)
            if query:
                await get_timetable_pdf(query, height, pdf)
            else:
                pdf.set_text_color(0, 128, 0)
                pdf.cell(100, height, 'ВЫХОДНОЙ', 0, 1, 'J')
                pdf.set_text_color(0, 0, 10)
            pdf.set_text_color(0, 128, 0)
            pdf.cell(100, height, '*-' * 20, 0, 1, 'J')
            pdf.set_text_color(0, 0, 10)
    pdf.output(f'data/text{call.message.chat.id}.pdf')
    doc = open(f'data/text{call.message.chat.id}.pdf', mode='rb')
    await call.message.answer_document(doc)
    doc.close()
    await WorkTimeTable.table_work.set()
    await remove_pdf('data')
    await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
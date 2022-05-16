import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from fpdf import FPDF

from handlers.users.manager import remove_pdf
from handlers.users.models import TimeTable
from keyboard.nav import kb_table_menu
from loader import dp
from state.states import WorkTimeTable


@dp.message_handler(text='Посмотреть график', state=WorkTimeTable.table_work)
async def view_chart(message: types.Message):
    kb_chart = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
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
    # Add a page
    pdf.add_page()
    # set style and size of font
    # that you want in the pdf
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

        for item in query:
            if item.free == False:
                for i in item.records:
                    pdf.set_text_color(255, 0, 0)
                    row = (item.time_zone, i.service, i.cunsomer_user.first_name)
                    for x, y in enumerate(row):
                        if x == 0:
                            pdf.set_font("FreeSansBo", style='B', size=18)
                            pdf.set_text_color(255, 0, 0)
                            pdf.cell(20, height, y, 0, 0, 'J')
                            pdf.set_font("FreeSans", size=20)
                        elif x == 1:
                            pdf.set_text_color(0, 128, 0)
                            pdf.cell(100, height, y, 0, 0, 'J')
                        elif x == 2:
                            pdf.set_text_color(0, 0, 10)
                            pdf.cell(20, height, y, 0, 1, 'J')

            else:
                row = (item.time_zone, 'свободно')
                for x, y in enumerate(row):
                    if x == 0:
                        pdf.set_font("FreeSansBo", style='B', size=18)
                        pdf.set_text_color(255, 0, 0)
                        pdf.cell(20, height, y, 0, 0, 'J')
                        pdf.set_font("FreeSans", size=20)

                    elif x == 1:
                        pdf.set_text_color(0, 0, 10)
                        pdf.cell(100, height, y, 0, 1, 'J')
        # pdf.output(f'data/text{call.message.chat.id}.pdf')
        # doc = open(f'data/text{call.message.chat.id}.pdf', mode='rb')
        # await call.message.answer_document(doc)
        # doc.close()
        # await WorkTimeTable.table_work.set()
        # await remove_pdf('data')
        # await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
    elif call.data == 'week':
        for day in range(1, 8):
            pdf.set_font("FreeSans", size=20)
            pdf.set_text_color(255, 0, 0)
            d = (datetime.datetime.today() + datetime.timedelta(days=day)).date()
            date_str = datetime.datetime.strftime(d, '%d.%m')
            text = f'График на {date_str}'
            pdf.cell(100, 20, text, 0, 1, 'L')
            query = TimeTable.select().where(TimeTable.day == d)
            if query:
                for item in query:
                    if item.free == False:
                        for i in item.records:
                            pdf.set_text_color(255, 0, 0)
                            row = (item.time_zone, i.service, i.cunsomer_user.first_name)
                            for x, y in enumerate(row):
                                if x == 0:
                                    pdf.set_font("FreeSansBo", style='B', size=18)
                                    pdf.set_text_color(255, 0, 0)
                                    pdf.cell(20, height, y, 0, 0, 'J')
                                    pdf.set_font("FreeSans", size=20)
                                elif x == 1:
                                    pdf.set_text_color(0, 128, 0)
                                    pdf.cell(100, height, y, 0, 0, 'J')
                                elif x == 2:
                                    pdf.set_text_color(0, 0, 10)
                                    pdf.cell(20, 15, y, 0, 1, 'J')

                    else:
                        row = (item.time_zone, 'свободно')
                        for x, y in enumerate(row):
                            if x == 0:
                                pdf.set_font("FreeSansBo", style='B', size=18)
                                pdf.set_text_color(255, 0, 0)
                                pdf.cell(20, height, y, 0, 0, 'J')
                                pdf.set_font("FreeSans", size=20)

                            elif x == 1:
                                pdf.set_text_color(0, 0, 10)
                                pdf.cell(100, height, y, 0, 1, 'J')
            else:
                pdf.set_text_color(0, 128, 0)
                pdf.cell(100, height, 'ВЫХОДНОЙ', 0, 1, 'J')
                pdf.set_text_color(0, 0, 10)
            pdf.set_text_color(0, 128, 0)
            pdf.cell(100, height, '*-' * 20, 0, 1, 'J')
            pdf.set_text_color(0, 0, 10)
        # pdf.output(f'data/text{call.message.chat.id}.pdf')
        # doc = open(f'data/text{call.message.chat.id}.pdf', mode='rb')
        # await call.message.answer_document(doc)
        # doc.close()
        # await WorkTimeTable.table_work.set()
        # await remove_pdf('data')
        # await call.message.answer('Работа с графиком', reply_markup=kb_table_menu)
    elif call.data == 'totally':
        for day in range(1, 22):
            pdf.set_font("FreeSans", size=20)
            pdf.set_text_color(255, 0, 0)
            d = (datetime.datetime.today() + datetime.timedelta(days=day)).date()
            date_str = datetime.datetime.strftime(d, '%d.%m')
            text = f'График на {date_str}'
            pdf.cell(100, 20, text, 0, 1, 'L')
            query = TimeTable.select().where(TimeTable.day == d)
            if query:
                for item in query:
                    if item.free == False:
                        for i in item.records:
                            pdf.set_text_color(255, 0, 0)
                            row = (item.time_zone, i.service, i.cunsomer_user.first_name)
                            for x, y in enumerate(row):
                                if x == 0:
                                    pdf.set_font("FreeSansBo", style='B', size=18)
                                    pdf.set_text_color(255, 0, 0)
                                    pdf.cell(20, height, y, 0, 0, 'J')
                                    pdf.set_font("FreeSans", size=20)
                                elif x == 1:
                                    pdf.set_text_color(0, 128, 0)
                                    pdf.cell(100, height, y, 0, 0, 'J')
                                elif x == 2:
                                    pdf.set_text_color(0, 0, 10)
                                    pdf.cell(20, 15, y, 0, 1, 'J')

                    else:
                        row = (item.time_zone, 'свободно')
                        for x, y in enumerate(row):
                            if x == 0:
                                pdf.set_font("FreeSansBo", style='B', size=18)
                                pdf.set_text_color(255, 0, 0)
                                pdf.cell(20, height, y, 0, 0, 'J')
                                pdf.set_font("FreeSans", size=20)

                            elif x == 1:
                                pdf.set_text_color(0, 0, 10)
                                pdf.cell(100, height, y, 0, 1, 'J')
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
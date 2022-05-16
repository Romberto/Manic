from aiogram import types
from aiogram.dispatcher import FSMContext
import datetime

from fpdf import FPDF

from handlers.users.manager import remove_pdf, date_to_str
from handlers.users.models import RecordRegistration, TimeTable
from keyboard.nav import kb_table_menu
from loader import dp
from state.states import WorkTimeTable


@dp.message_handler(text='Посмотреть записи', state=WorkTimeTable.table_work)
async def view_all_record(message: types.Message, state: FSMContext):
    today = datetime.datetime.today().date()
    rr = RecordRegistration.select()
    pdf = FPDF()
    # Add a page
    pdf.add_page()
    # set style and size of font
    # that you want in the pdf
    pdf.add_font('FreeSans', '', r'fonts/FreeSans.ttf', uni=True)
    pdf.add_font('FreeSansBo', 'B', r'fonts/FreeSansBold.ttf', uni=True)
    height = 12
    today = datetime.datetime.today().date()
    rr = TimeTable.select().order_by(TimeTable.day)
    for i in rr:
        if i.day > today:
            if i.records:
                for item in i.records:
                    row = (i.day, i.time_zone, item.service)
                    for x, y in enumerate(row):
                        if x == 0:
                            y = await date_to_str(y)
                            pdf.set_font("FreeSans", size=20)
                            pdf.set_text_color(255, 0, 10)
                            pdf.cell(20, 15, y, 0, 0, 'J')

                        elif x == 1:
                            pdf.set_font("FreeSans", size=20)
                            pdf.set_text_color(0, 0, 10)
                            pdf.cell(20, 15, y, 0, 0, 'J')
                        elif x == 2:
                            pdf.set_font("FreeSans", size=20)
                            pdf.set_text_color(0, 0, 10)
                            pdf.cell(20, 15, y, 0, 1, 'J')
        else:
            i.delete_instance()
    pdf.output(f'data/text{message.chat.id}.pdf')
    doc = open(f'data/text{message.chat.id}.pdf', mode='rb')
    await message.answer_document(doc)
    doc.close()
    await WorkTimeTable.table_work.set()
    await remove_pdf('data')
    await message.answer('Работа с графиком', reply_markup=kb_table_menu)

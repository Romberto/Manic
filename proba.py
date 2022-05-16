from data.config import SERVISES
from handlers.users.models import TimeTable, Users, RecordRegistration
from handlers.users.manager import TimeManager, data_str, str_to_date
from datetime import datetime
import datetime
import calendar
from fpdf import FPDF


def date_to_str(date):
    date_str = datetime.datetime.strftime(date, '%d.%m')
    return date_str


def set_date(s):
    pdf = FPDF()

    # Add a page
    pdf.add_page()
    # set style and size of font
    # that you want in the pdf
    pdf.add_font('FreeSans', '', r'fonts/FreeSans.ttf', uni=True)
    pdf.add_font('FreeSansBo', 'B', r'fonts/FreeSansBold.ttf', uni=True)
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
                        pdf.cell(20, 15, y, 0, 0, 'J')
                        pdf.set_font("FreeSans", size=20)
                    elif x == 1:
                        pdf.set_text_color(0, 128, 0)
                        pdf.cell(100, 15, y, 0, 0, 'J')
                    elif x == 2:
                        pdf.set_text_color(0, 0, 10)
                        pdf.cell(20, 15, y, 0, 1, 'J')

        else:
            row = (item.time_zone, 'свободно')
            for x, y in enumerate(row):
                if x == 0:
                    pdf.set_font("FreeSansBo", style='B', size=18)
                    pdf.set_text_color(255, 0, 0)
                    pdf.cell(20, 15, y, 0, 0, 'J')
                    pdf.set_font("FreeSans", size=20)

                elif x == 1:
                    pdf.set_text_color(0, 0, 10)
                    pdf.cell(100, 15, y, 0, 1, 'J')

    pdf.output('text.pdf')


if __name__ == '__main__':
    set_date('tomorrow')

import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from fpdf import FPDF

from data.config import MASTER
from handlers.users.manager import date_to_str, remove_pdf
from handlers.users.models import TimeTable, RecordRegistration, Users
from loader import dp
import asyncio
import aioschedule


async def noon_print():
    # удаляем устаревшие записи
    today = datetime.datetime.today().date()
    query = TimeTable.select().where(TimeTable.day < today)
    if query:
        for item in query:
            item.delete_instance()
    # делаем запрос на завтра
    check_date = today + datetime.timedelta(days=1)
    query = TimeTable.select().where(TimeTable.day == check_date)
    if query:
        for elem in query:
            for record in elem.records:
                chat_id = record.cunsomer_user.chat_id
                service = record.cunsomer_user.service
                first_name = record.cunsomer_user.first_name
                date = await date_to_str(check_date)
                time = elem.time_zone
                text_client = f"{first_name} напоминаю, \nзавтра {date} вы записаны на {service}, " \
                              f"мастер ждёт вас в {time} "
                # отправляем клиенту сообщение о том , что  он записан на завтра
                await dp.bot.send_message(chat_id=chat_id, text=text_client)
        # отправляем мастеру график на завтра
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('FreeSans', '', r'fonts/FreeSans.ttf', uni=True)
        pdf.add_font('FreeSansBo', 'B', r'fonts/FreeSansBold.ttf', uni=True)
        height = 12
        # формируем заголовок
        pdf.set_font("FreeSans", size=20)
        pdf.set_text_color(255, 0, 0)
        tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
        date_str = datetime.datetime.strftime(tomorrow, '%d.%m')
        text = f'График на {date_str}'
        pdf.cell(100, 20, text, 0, 1, 'L')
        for item in query:
            if not item.free:
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
        pdf.output(f'data/ras_tomorrow.pdf')
        doc = open(f'data/ras_tomorrow.pdf', mode='rb')
        # посылаем сообщение в виде расписания на завтра, мастеру
        await dp.bot.send_document(chat_id=MASTER, document=doc)
        doc.close()
        await remove_pdf('data')


async def check_confirm():
    rr = RecordRegistration.select().where(RecordRegistration.confirm == False).first()
    if rr:
        user = rr.cunsomer_user
        tt = TimeTable.select().join(RecordRegistration).where(RecordRegistration.confirm == False,
                                                               RecordRegistration.cunsomer_user == user).first()
        d = await date_to_str(tt.day)
        t = tt.time_zone
        kb_confirm = types.InlineKeyboardMarkup()
        buttons = [types.InlineKeyboardButton(text='подтвердить', callback_data=f'{user} {d} {t}')]
        kb_confirm.add(*buttons)
        await dp.bot.send_message(chat_id=MASTER, text='НОВАЯ ЗАПИСЬ \n'
                                                       f'Клиент {user.first_name} {user.last_name} '
                                                       f'внёс предоплату за '
                                                       f'{rr.service}\n'
                                                       f'на {d} {t}', reply_markup=kb_confirm)


async def scheduler():
    aioschedule.every().day.at("18:00").do(noon_print)
    aioschedule.every(30).minutes.do(check_confirm)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def check_rec():
    asyncio.create_task(scheduler())

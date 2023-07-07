import os

from connections import bot, DbUtils


def remind_today(chat_id: str):
    db_cursor = DbUtils()
    fetched_records = db_cursor.get_items(
        f"select * from schedule where id=(select cast (strftime('%w', '2022-01-01') as integer) + 1);"
    )[0]
    remind_text = os.getenv('REMIND_TEXT') % fetched_records[1:]
    bot.send_message(chat_id, remind_text)


def remind_all_services(chat_id: str):
    db_cursor = DbUtils()
    fetched_records = db_cursor.get_items(
        f"select weekday, weekday_dt, leading, leading_dl, attendant, attendant_dl, cleaner, cleaner_dl from schedule;"
    )
    all_services_text = []
    for rec in fetched_records:
        rec = [' '.join(el) for el in list(zip(os.getenv('ALL_SERVICES_MAPPER').split(','), rec))]
        all_services_text.append(f"{rec[0]} {rec[1]}\n{rec[2]} {rec[3]}\n{rec[4]} {rec[5]}\n{rec[6]} {rec[7]}")
    bot.send_message(chat_id, '\n\n'.join(all_services_text))


if __name__ == '__main__':
    remind_today(os.getenv('WORK_CHAT'))

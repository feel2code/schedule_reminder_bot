import os

from connections import bot, DbUtils
from reminder import remind_all_services, remind_today


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Catching text messages or commands for bot."""
    if message.chat.id == int(os.getenv('WORK_CHAT')):
        if message.text == '/update_service':
            bot.send_message(message.chat.id, os.getenv('UPDATE_TEXT'))
            bot.register_next_step_handler(message, update_service)
        elif message.text == '/all_service':
            remind_all_services(message.chat.id)
        elif message.text == '/service':
            remind_today(message.chat.id)
        elif message.text == '/update_service_all':
            pass


def update_service(message):
    try:
        weekday, role, servant, nick, dl = message.text.replace(' ', '').split(',')
        iterator = iter(os.getenv("SERVICE_MAPPER").split(','))
        role_map = dict(zip(iterator, iterator))
        service = role_map[role]
        db_cursor = DbUtils()
        db_cursor.update_items(
            f"update schedule set {service}='{servant} {nick}', {service}_dl='{dl}' where weekday='{weekday}';"
        )
        bot.send_message(message.chat.id, os.getenv('SUCCESSFULLY_UPDATE_TEXT'))
    except ValueError:
        bot.send_message(message.chat.id, os.getenv('ERROR_TEXT'))


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0, timeout=500)

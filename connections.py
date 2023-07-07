import os
import sqlite3

import telebot

from dotenv import load_dotenv

load_dotenv(".env")
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))


class DbUtils:
    def __init__(self, dbname=os.getenv('DATABASE')):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def update_items(self, request):
        self.conn.execute(request)
        self.conn.commit()

    def get_items(self, request):
        return [x for x in self.conn.execute(request)]

#Developed By Mr.Amini
#My Telegram ID: @MrAminiNehad
#My Github: https://github.com/MrAminiNezhad/
#Code version 1.1.2

import logging
import requests
import json
import os
from datetime import datetime
from persiantools.jdatetime import JalaliDateTime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

TOKEN = 'Your_Token'
Panel_URL = 'Panel_Adress:Port' #Example https://mypanel.com:2080
Panel_USER = 'UserName'
Panel_PASS = 'PassWord'
Support_text = 'متن پشتیبانی شما'

COOKIES_FILE = 'cookies.txt' # Don't Change

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.handle_message))
        self.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback_query))

        self.session = requests.Session()
        self.waiting_for_connection = False

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="به ربات نمایش حجم خوش آمدید")

        keyboard = [
            [InlineKeyboardButton("مشاهده حجم", callback_data='view_volume')],
            [InlineKeyboardButton("پشتیبانی", callback_data='support')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('لطفاً یک گزینه را انتخاب کنید:', reply_markup=reply_markup)

        if self.check_cookies():
            os.remove(COOKIES_FILE)

    def handle_message(self, update, context):
        text = update.message.text

        if self.waiting_for_connection:
            self.waiting_for_connection = False
            volume_message = self.get_volume(text)
            context.bot.send_message(chat_id=update.effective_chat.id, text=volume_message)
        else:
            if text == 'مشاهده حجم':
                context.bot.send_message(chat_id=update.effective_chat.id, text="لطفاً نام کانکشن خود را ارسال فرمایید")

    def handle_callback_query(self, update, context):
        query = update.callback_query
        query.answer()  # پاسخ به کوئری دکمه شیشه‌ای

        if query.data == 'view_volume':
            self.waiting_for_connection = True
            context.bot.send_message(chat_id=update.effective_chat.id, text="لطفاً نام کانکشن خود را ارسال فرمایید")

        elif query.data == 'support':
            context.bot.send_message(chat_id=update.effective_chat.id, text= f"{Support_text}")

    def get_volume(self, connection_name):
        if not self.check_cookies():
            self.run_login_script()

        url = f"{Panel_URL}/panel/api/inbounds/getClientTraffics/{connection_name}"
        response = self.session.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)

            if data['obj'] is None:
                return "نام کاربری وارد شده صحیح نمی باشد لطفا مجدد تلاش کنید"

            down = data['obj']['down']
            up = data['obj']['up']
            total = data['obj']['total']

            down_gigabit = self.convert_to_gigabit(down)
            up_gigabit = self.convert_to_gigabit(up)
            total_gigabit = self.convert_to_gigabit(total)

            expiry_time = self.get_expiry_time(data)

            volume_message = f"مقدار دانلود: {down_gigabit} GB\nمقدار آپلود: {up_gigabit} GB\nمجموع مصرف: {(down_gigabit + up_gigabit)} GB\nحجم باقی مانده: {total_gigabit - (down_gigabit + up_gigabit)} GB\nتاریخ انقضا: {expiry_time}"
            return volume_message
        else:
            return "دریافت اطلاعات امکان‌پذیر نیست"

    def check_cookies(self):
        try:
            with open(COOKIES_FILE, 'r') as file:
                return True
        except FileNotFoundError:
            return False

    def run_login_script(self):
        url = f"{Panel_URL}/login"
        data = {
            'username': Panel_USER,
            'password': Panel_PASS
        }

        response = self.session.post(url, data=data)

        if response.status_code == 200:
            with open(COOKIES_FILE, 'w') as file:
                file.write(response.text)

    def convert_to_gigabit(self, value):
        gigabit = round(value / 1024 / 1024 / 1024, 2)
        return gigabit

    def get_expiry_time(self, data):
        expiry_time = data['obj']['expiryTime']
        expiry_datetime = datetime.fromtimestamp(expiry_time / 1000)
        jalali_expiry = JalaliDateTime.to_jalali(expiry_datetime)
        expiry_time_str = f"{jalali_expiry.year}/{jalali_expiry.month}/{jalali_expiry.day} {expiry_datetime.strftime('%H:%M:%S')}"
        return expiry_time_str

    def start_bot(self):
        self.updater.start_polling()

    def stop_bot(self):
        self.updater.stop()


bot = TelegramBot(TOKEN)
bot.start_bot()

#Developed By Mr.Amini
#My Telegram ID: @MrAminiNehad
#My Github: https://github.com/MrAminiNezhad/
#Code version 1.1.2

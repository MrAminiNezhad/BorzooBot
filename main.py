#Developed By Mr.Amini
#My Telegram ID: @MrAminiNehad
#My Github: https://github.com/MrAminiNezhad/
#Code version 1.2.1


import logging
import requests
import json
import os
from datetime import datetime
from persiantools.jdatetime import JalaliDateTime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

COOKIES_FILE = 'cookies.txt'

class TelegramBot:
    def __init__(self, token, panel_url, panel_user, panel_pass, support_text, admin_id, welcome_text):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.handle_message))
        self.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback_query))

        self.session = requests.Session()
        self.waiting_for_connection = False
        self.waiting_for_message = False

        self.panel_url = panel_url
        self.panel_user = panel_user
        self.panel_pass = panel_pass
        self.support_text = support_text
        self.admin_id = admin_id
        self.welcome_text = welcome_text

        self.create_user_file()

    def create_user_file(self):
        user_file_path = 'user.txt'
        if not os.path.isfile(user_file_path):
            with open(user_file_path, 'w') as file:
                pass

    def start(self, update, context):
        user_id = update.effective_chat.id

        context.bot.send_message(chat_id=user_id, text=self.welcome_text)

        if self.is_admin(user_id):
            keyboard = [
                [InlineKeyboardButton("مشاهده حجم", callback_data='view_volume')],
                [InlineKeyboardButton("پشتیبانی", callback_data='support')],
                [InlineKeyboardButton("ارسال پیام همگانی", callback_data='send_message')]
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("مشاهده حجم", callback_data='view_volume')],
                [InlineKeyboardButton("پشتیبانی", callback_data='support')]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('لطفاً یک گزینه را انتخاب کنید:', reply_markup=reply_markup)

        if self.check_cookies():
            os.remove(COOKIES_FILE)

        self.save_user_id(user_id)

    def handle_message(self, update, context):
        text = update.message.text

        if self.waiting_for_connection:
            self.waiting_for_connection = False
            volume_message = self.get_volume(text)
            context.bot.send_message(chat_id=update.effective_chat.id, text=volume_message)
        elif self.waiting_for_message:
            if self.is_admin(update.effective_chat.id):
                self.waiting_for_message = False
                user_ids = self.get_all_user_ids()
                success_count = 0
                failure_count = 0
                for user_id in user_ids:
                    try:
                        context.bot.send_message(chat_id=user_id, text=text)
                        success_count += 1
                    except Exception:
                        failure_count += 1
                admin_message = f"ارسال پیام با موفقیت به پایان رسید\nتعداد کل کاربران ربات: {len(user_ids)}\nتعداد ارسال موفق: {success_count}\nتعداد ارسال ناموفق: {failure_count}"
                context.bot.send_message(chat_id=self.admin_id, text=admin_message)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="شما اجازه دسترسی به این عملیات را ندارید.")
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
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.support_text)

        elif query.data == 'send_message':
            if self.is_admin(update.effective_chat.id):
                context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا پیام مورد نظر خود را ارسال بکنید تا برای تمامی کاربران ارسال شود")
                self.waiting_for_message = True
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="شما اجازه دسترسی به این عملیات را ندارید.")

    def get_volume(self, connection_name):
        if not self.check_cookies():
            self.run_login_script()

        url = f"{self.panel_url}/panel/api/inbounds/getClientTraffics/{connection_name}"
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
        url = f"{self.panel_url}/login"
        data = {
            'username': self.panel_user,
            'password': self.panel_pass
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

    def save_user_id(self, user_id):
        if not self.is_duplicate_user(user_id):
            with open('user.txt', 'a') as file:
                file.write(str(user_id) + '\n')
        else:
            print("آی‌دی کاربر تکراری است و اضافه نشد.")

    def is_duplicate_user(self, user_id):
        user_ids = self.get_all_user_ids()
        return str(user_id) in user_ids

    def get_all_user_ids(self):
        with open('user.txt', 'r') as file:
            user_ids = [line.strip() for line in file]

        return user_ids

    def is_admin(self, user_id):
        return str(user_id) == str(self.admin_id)


def read_info_from_file():
    with open('info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    token = data['TOKEN']
    panel_url = data['Panel_URL']
    panel_user = data['Panel_USER']
    panel_pass = data['Panel_PASS']
    support_text = data['Support_text']
    admin_id = data['admin_id']
    welcome_text = data['welcome_text']

    return token, panel_url, panel_user, panel_pass, support_text, admin_id, welcome_text


TOKEN, Panel_URL, Panel_USER, Panel_PASS, Support_text, Admin_ID, Welcome_text = read_info_from_file()

bot = TelegramBot(TOKEN, Panel_URL, Panel_USER, Panel_PASS, Support_text, Admin_ID, Welcome_text)
bot.start_bot()


#Developed By Mr.Amini
#My Telegram ID: @MrAminiNehad
#My Github: https://github.com/MrAminiNezhad/
#Code version 1.2.1

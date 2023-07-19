#Developed By Mr.Amini
#My Telegram ID: @MrAminiNehad
#My Github: https://github.com/MrAminiNezhad/
#Code version 1.3.1

import logging
import requests
import json
import os
from datetime import datetime
from persiantools.jdatetime import JalaliDateTime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

COOKIES_DIRECTORY = 'cookies'

class TelegramBot:
    def __init__(self, token, panels, support_text, admin_ids, welcome_text):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.handle_message))
        self.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback_query))

        self.session = requests.Session()
        self.waiting_for_connection = False
        self.waiting_for_message = False

        self.panels = panels
        self.support_text = support_text
        self.admin_ids = admin_ids
        self.welcome_text = welcome_text

        self.create_user_file()
        self.create_cookies_directory()

    def create_user_file(self):
        user_file_path = 'user.txt'
        if not os.path.isfile(user_file_path):
            with open(user_file_path, 'w') as file:
                pass

    def create_cookies_directory(self):
        if not os.path.exists(COOKIES_DIRECTORY):
            os.makedirs(COOKIES_DIRECTORY)

    def start(self, update, context):
        user_id = update.effective_chat.id

        context.bot.send_message(chat_id=user_id, text=self.welcome_text, parse_mode='Markdown')

        if self.is_admin(user_id):
            keyboard = [
                [InlineKeyboardButton("مشاهده حجم", callback_data='view_volume')],
                [InlineKeyboardButton("پشتیبانی", callback_data='support')],
                [InlineKeyboardButton("ارسال پیام همگانی", callback_data='send_message')],
                [InlineKeyboardButton("آمار کاربران ربات", callback_data='user_stats')],
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("مشاهده حجم", callback_data='view_volume')],
                [InlineKeyboardButton("پشتیبانی", callback_data='support')]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('لطفاً یک گزینه را انتخاب کنید:', reply_markup=reply_markup)

        if self.check_cookies():
            self.remove_cookies()

        self.save_user_id(user_id)

    def handle_message(self, update, context):
        text = update.message.text

        if self.waiting_for_connection:
            self.waiting_for_connection = False
            volume_message = self.get_volume(text)
            if isinstance(volume_message, tuple):
                context.bot.send_message(chat_id=update.effective_chat.id, text=volume_message[0], parse_mode='Markdown', reply_markup=volume_message[1])
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=volume_message, parse_mode='Markdown')
        elif self.waiting_for_message:
            if self.is_admin(update.effective_chat.id):
                self.waiting_for_message = False
                user_ids = self.get_all_user_ids()
                success_count = 0
                failure_count = 0
                for user_id in user_ids:
                    try:
                        context.bot.send_message(chat_id=user_id, text=text, parse_mode='Markdown')
                        success_count += 1
                    except Exception:
                        failure_count += 1
                admin_message = f"ارسال پیام با موفقیت به پایان رسید\nتعداد کل کاربران ربات: {len(user_ids)}\nتعداد ارسال موفق: {success_count}\nتعداد ارسال ناموفق: {failure_count}"
                context.bot.send_message(chat_id=self.admin_ids[0], text=admin_message, parse_mode='Markdown')
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="شما اجازه دسترسی به این عملیات را ندارید.")
        else:
            if text == 'مشاهده حجم':
                context.bot.send_message(chat_id=update.effective_chat.id, text="لطفاً نام کانکشن خود را ارسال فرمایید")

    def handle_callback_query(self, update, context):
        query = update.callback_query
        query.answer()

        if query.data == 'view_volume':
            self.waiting_for_connection = True
            context.bot.send_message(chat_id=update.effective_chat.id, text="لطفاً نام کانکشن خود را ارسال فرمایید")

        elif query.data == 'support':
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.support_text, parse_mode='Markdown')

        elif query.data == 'send_message':
            if self.is_admin(update.effective_chat.id):
                self.waiting_for_message = True
                context.bot.send_message(chat_id=update.effective_chat.id, text="لطفا پیام مورد نظر خود را ارسال بکنید تا برای تمامی کاربران ارسال شود")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="شما اجازه دسترسی به این عملیات را ندارید.")

        elif query.data == 'user_stats':
            if self.is_admin(update.effective_chat.id):
                user_count = len(self.get_all_user_ids())
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"تعداد کل کاربران ربات: {user_count}")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="شما اجازه دسترسی به این عملیات را ندارید.")

    def get_volume(self, connection_name):
        if not self.check_cookies():
            self.run_login_scripts()

        volume_message = ""
        reply_markup = None

        for panel in self.panels:
            panel_url = panel['panel_url']
            panel_user = panel['panel_user']
            panel_pass = panel['panel_pass']
            cookies_file = panel['cookies_file']
            connection = panel['connection_name']

            if connection_name == connection:
                url = f"{panel_url}/panel/api/inbounds/getClientTraffics/{connection_name}"
                response = self.session.get(url, cookies=self.load_cookies(cookies_file))

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

                    acc_status = data['obj']['enable']
                    acc_status_message = "فعال ✅" if acc_status else "غیر فعال ❌"

                    keyboard = [
                        [InlineKeyboardButton(f"وضعیت اکانت: {acc_status_message}", callback_data='acc_status')],
                        [InlineKeyboardButton(f"مقدار دانلود: {down_gigabit:.2f} GB ⬇", callback_data='download')],
                        [InlineKeyboardButton(f"مقدار آپلود: {up_gigabit:.2f} GB ⬆", callback_data='upload')],
                        [InlineKeyboardButton(f"مجموع مصرف: {(down_gigabit + up_gigabit):.2f} GB ⏳", callback_data='total')],
                        [InlineKeyboardButton(f"حجم کل: {total_gigabit:.2f} GB 🔋", callback_data='total')],
                        [InlineKeyboardButton(f"حجم باقی مانده: {float(total_gigabit) - (float(down_gigabit) + float(up_gigabit)):.2f} GB 📡", callback_data='traffic_remaining')],
                        [InlineKeyboardButton(f"تاریخ انقضا: {expiry_time} 🔚", callback_data='expiry')],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    volume_message += f"وضعیت اکانت {connection} به شرح زیر می‌باشد:\n"
                    volume_message += f"مقدار دانلود: {down_gigabit:.2f} GB ⬇\n"
                    volume_message += f"مقدار آپلود: {up_gigabit:.2f} GB ⬆\n"
                    volume_message += f"مجموع مصرف: {(down_gigabit + up_gigabit):.2f} GB ⏳\n"
                    volume_message += f"حجم کل: {total_gigabit:.2f} GB 🔋\n"
                    volume_message += f"حجم باقی مانده: {float(total_gigabit) - (float(down_gigabit) + float(up_gigabit)):.2f} GB 📡\n"
                    volume_message += f"تاریخ انقضا: {expiry_time} 🔚\n\n"
                else:
                    volume_message += f"دریافت اطلاعات از پنل {connection} امکان‌پذیر نیست\n\n"

        return volume_message, reply_markup

    def check_cookies(self):
        return all([self.check_cookies_file(panel['cookies_file']) for panel in self.panels])

    def check_cookies_file(self, cookies_file):
        return os.path.isfile(self.get_cookies_file_path(cookies_file))

    def remove_cookies(self):
        for panel in self.panels:
            cookies_file = panel['cookies_file']
            cookies_file_path = self.get_cookies_file_path(cookies_file)
            if os.path.exists(cookies_file_path):
                os.remove(cookies_file_path)

    def run_login_scripts(self):
        for panel in self.panels:
            panel_url = panel['panel_url']
            panel_user = panel['panel_user']
            panel_pass = panel['panel_pass']
            cookies_file = panel['cookies_file']

            url = f"{panel_url}/login"
            data = {
                'username': panel_user,
                'password': panel_pass
            }

            response = self.session.post(url, data=data)

            if response.status_code == 200:
                with open(self.get_cookies_file_path(cookies_file), 'w') as file:
                    file.write(response.text)

    def load_cookies(self, cookies_file):
        cookies = requests.cookies.RequestsCookieJar()
        cookies_file_path = self.get_cookies_file_path(cookies_file)

        if os.path.isfile(cookies_file_path):
            with open(cookies_file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        name, value = line.split('\t', maxsplit=6)[:2]
                        cookies.set(name, value)

        return cookies

    def get_cookies_file_path(self, cookies_file):
        return os.path.join(COOKIES_DIRECTORY, cookies_file)

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

    def is_duplicate_user(self, user_id):
        user_ids = self.get_all_user_ids()
        return str(user_id) in user_ids

    def get_all_user_ids(self):
        with open('user.txt', 'r') as file:
            user_ids = [line.strip() for line in file]

        return user_ids

    def is_admin(self, user_id):
        return str(user_id) in map(str, self.admin_ids)


def read_info_from_file():
    with open('info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    token = data['TOKEN']
    panels = data['panels']
    support_text = data['Support_text']
    welcome_text = data['welcome_text']
    admin_ids = data['admin_ids']

    return token, panels, support_text, admin_ids, welcome_text


def main():
    token, panels, support_text, admin_ids, welcome_text = read_info_from_file()
    bot = TelegramBot(token, panels, support_text, admin_ids, welcome_text)
    bot.start_bot()


if __name__ == '__main__':
    main()



#Developed By Mr.Amini
#My Telegram ID: @MrAminiNehad
#My Github: https://github.com/MrAminiNezhad/
#Code version 1.3.1

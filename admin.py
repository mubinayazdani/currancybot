import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

ADMINS = [5485623939, 5304632888]  

def is_admin(user_id):
    return user_id in ADMINS

def setup_admin_panel(bot):
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        user_id = message.from_user.id
        if is_admin(user_id):
            markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            btn1 = KeyboardButton("📋 تعداد کاربران")
            btn2 = KeyboardButton("📊 تعداد درخواست‌ها")
            btn3 = KeyboardButton("⏹ خروج از پنل")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, "به پنل ادمین خوش آمدید:", reply_markup=markup)
        else:
            bot.reply_to(message, "❌ شما اجازه دسترسی به این بخش را ندارید.")

    @bot.message_handler(func=lambda message: is_admin(message.from_user.id) and message.text == "📋 تعداد کاربران")
    def show_user_count(message):
        try:
            conn = sqlite3.connect('btcn.db')  
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            conn.close()
            bot.reply_to(message, f"👥 تعداد کل کاربران: {user_count}")
        except Exception as e:
            bot.reply_to(message, "⚠️ خطایی رخ داد.")
            print(f"Error: {e}")

    @bot.message_handler(func=lambda message: is_admin(message.from_user.id) and message.text == "📊 تعداد درخواست‌ها")
    def show_total_requests(message):
        try:
            conn = sqlite3.connect('btcn.db')  
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(request) FROM users")
            total_requests = cursor.fetchone()[0]
            conn.close()

            if total_requests is not None:
                bot.reply_to(message, f"📊 تعداد کل درخواست‌ها: {total_requests}")
            else:
                bot.reply_to(message, "📭 هنوز هیچ درخواستی ثبت نشده است.")
        except Exception as e:
            bot.reply_to(message, "⚠️ خطایی رخ داد.")
            print(f"Error: {e}")

    # @bot.message_handler(func=lambda message: is_admin(message.from_user.id) and message.text == "📛 قفل چنل")
    # def lock_channel(message):
    #     try:
    #     # ذخیره وضعیت قفل بودن چنل در پایگاه داده یا فایل
    #         conn = sqlite3.connect('btcn.db')
    #         cursor = conn.cursor()
        
    #     # به‌روز رسانی وضعیت قفل چنل در پایگاه داده
    #         cursor.execute("UPDATE settings SET channel_locked = 1 WHERE id = 1")
    #         conn.commit()
    #         conn.close()

    #         bot.reply_to(message, "✅ چنل قفل شد. کاربران نمی‌توانند درخواست ارسال کنند.")

    #     except Exception as e:
    #         bot.reply_to(message, "⚠️ خطا در قفل کردن چنل.")
    #         print(f"Error: {e}")



    @bot.message_handler(func=lambda message: is_admin(message.from_user.id) and message.text == "⏹ خروج از پنل")
    def exit_admin_panel(message):
        bot.send_message(message.chat.id, "پنل ادمین بسته شد.", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True))

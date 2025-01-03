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
            conn = sqlite3.connect('btnc.db')  
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            conn.close()
            bot.reply_to(message, f"👥 تعداد کل کاربران: {user_count}")
        except Exception as e:
            bot.reply_to(message, "⚠️ خطایی رخ داد.")
            print(f"Error: {e}")

    # @bot.message_handler(func=lambda message: is_admin(message.from_user.id) and message.text == "📊 تعداد درخواست‌ها")
    # def show_user_requests(message):
    #     try:
    #         conn = sqlite3.connect('btnc.db') 
    #         cursor = conn.cursor()
    #         cursor.execute("SELECT id, requests FROM users")
    #         rows = cursor.fetchall()
    #         conn.close()
            
    #         if rows:
    #             response = "📊 تعداد درخواست‌ها:\n\n"
    #             for row in rows:
    #                 response += f"👤 کاربر {row[0]}: {row[1]} درخواست\n"
    #             bot.reply_to(message, response)
    #         else:
    #             bot.reply_to(message, "📭 هیچ کاربری یافت نشد.")
    #     except Exception as e:
    #         bot.reply_to(message, "⚠️ خطایی رخ داد.")
    #         print(f"Error: {e}")

    @bot.message_handler(func=lambda message: is_admin(message.from_user.id) and message.text == "⏹ خروج از پنل")
    def exit_admin_panel(message):
        bot.send_message(message.chat.id, "پنل ادمین بسته شد.", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True))

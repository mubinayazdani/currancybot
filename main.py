from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from database import add_user, get_user, create_tables
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import admin
import requests
import telebot
import io


create_tables()


API_TOKEN = '7633590311:AAF-f5LfHg5bb2R8cX3quvX17nvf3f3F2Pc'
NEWS_API_KEY = '565f2b98562f42c5ba010970199d4cc0'  
CHANNEL_USERNAME = 'flork_ir'
bot = telebot.TeleBot(API_TOKEN)

admin.setup_admin_panel(bot)


user_requests = {}

#limiting request function

def can_user_request(user_id):
    try:
        current_date = datetime.now().date()
        if user_id not in user_requests:
            user_requests[user_id] = {'date': current_date, 'count': 0}
        if user_requests[user_id]['date'] != current_date:
            user_requests[user_id] = {'date': current_date, 'count': 0}
        if user_requests[user_id]['count'] < 10:
            user_requests[user_id]['count'] += 1
            return True
        return False
    except Exception as e:
        print(f"خطا در بررسی محدودیت درخواست: {e}")
        return False


#checking if user is in channel

def is_user_member(user_id):
    try:

        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"خطا در بررسی عضویت: {e}")
        return False


#normalizing curruncies

def normalize_currency_name(currency_name):
    try:
        currency_name = currency_name.lower().strip()
        currency_name = currency_name.replace('‌', ' ')
        currency_name = currency_name.replace(' ', '')
        return currency_name
    except Exception as e:
        print(f"خطا در نرمال‌سازی نام ارز: {e}")
        return currency_name


currency_map = {
    
   
    "بیتکوین": "bitcoin",
    "بیت": "bitcoin",
    "اتریوم": "ethereum",
    "ریپل": "ripple",
    "دوجکوین": "dogecoin",
    "دوج": "dogecoin",
    "لایتکوین": "litecoin",
    "بایننسکوین": "binancecoin",
    "کاردانو": "cardano",
    "سولانا": "solana",
    "شیبا": "shiba-inu",
    "یونی‌سواپ": "uniswap",
    "تتر": "tether",
    "چینلینک": "chainlink",
    "استلار": "stellar",
    "ترا": "terra-luna",
    "ترون": "tron",
    "اولنچ": "avalanche-2",
    "پولکادات": "polkadot",
    "پانک": "punk",
    "فانتوم": "fantom",
    "آوالانچ": "avalanche-2",
    "مونرو": "monero",
    "تزوس": "tezos",
    "آلگوراند": "algorand",
    "تون":"the-open-network",
    "آوه": "aave",
    "میکر": "maker",
    "فایلکوین": "filecoin",
    "کوزاما": "kusama",
    "هارمونی": "harmony",
    "زیکش": "zcash",
    "دی‌سنترالند": "decentraland",
    "دش": "dash",
    "ورج": "verge",
    "آیوتا": "iota",
    "الروند": "elrond-erd-2",
    "اکسی اینفینیتی": "axie-infinity",
    "سندباکس": "the-sandbox",
    "ویچین": "vechain",
    "انجین کوین": "enjincoin",
    "گراف": "the-graph",
    "اردر": "ardor",
    "نیر پروتکل": "near",
    "گالا": "gala",
    "آربیتروم": "arbitrum",
    "هلیوم": "helium",
    "فلو": "flow",
    "اینترنت‌کامپیوتر": "internet-computer",
    "اوککس": "okb",
    "تونکوین": "the-open-network",
    "چیلز": "chiliz",
    "ریون‌کوین": "ravencoin",
    "همستر": "hamster",          
    "شیبا اینو": "shiba-inu",    
    "سیف مون": "safemoon",       
    "فگ": "feg-token",           
    "کیشو اینو": "kishu-inu",    
    "هوسکی": "husky",            
    "اکیتا": "akita-inu",        
    "بیبی دوج": "baby-doge-coin",
    "کیشو": "kishu-inu",         
    "پپه": "pepe"
}



def convert_currency_name(currency_name):
    try:
        currency_name = normalize_currency_name(currency_name)
        if currency_name in currency_map:
            return currency_map[currency_name]
        for key in currency_map:
            if currency_name in key:
                return currency_map[key]
        return currency_name
    except Exception as e:
        print(f"خطا در تبدیل نام ارز: {e}")
        return currency_name


#getting_price_url
COINGECKO_URL = 'https://api.coingecko.com/api/v3/simple/price'

# #converting_url
FIXER_URL = 'https://api.exchangerate-api.com/v4/latest/USD'

#price_history_url
HISTORY_URL = 'https://api.coingecko.com/api/v3/coins/{}/market_chart'


def is_user_member(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def create_main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn1 = KeyboardButton("💰 دریافت قیمت")
    btn2 = KeyboardButton("📉 تغییرات ۲۴ ساعته")
    btn3 = KeyboardButton("🔔 تنظیم هشدار")
    btn4 = KeyboardButton("📊 مقایسه ارزها")
    btn5 = KeyboardButton("📰 اخبار ارزهای دیجیتال")
    btn6 = KeyboardButton("📈 نمودار قیمت")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    add_user(user_id, username)
    if is_user_member(user_id):
        markup = create_main_menu()
        bot.send_message(message.chat.id, "یک گزینه را انتخاب کنید:", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        join_button = InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")
        check_button = InlineKeyboardButton("بررسی عضویت ✅", callback_data="check_membership")
        markup.add(join_button)
        markup.add(check_button)
        bot.send_message(
            message.chat.id,
            f"❗️ برای استفاده از این بات، ابتدا باید عضو کانال زیر شوید:\n@{CHANNEL_USERNAME}",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def check_membership(call):
    user_id = call.from_user.id
    if is_user_member(user_id):
        markup = create_main_menu()
        bot.send_message(call.message.chat.id, "عضویت شما تایید شد! اکنون می‌توانید از بات استفاده کنید.", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "❗️ هنوز عضو کانال نشده‌اید. لطفاً عضو شوید و دوباره امتحان کنید.", show_alert=True)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if not is_user_member(user_id):
        markup = InlineKeyboardMarkup()
        join_button = InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")
        check_button = InlineKeyboardButton("بررسی عضویت ✅", callback_data="check_membership")
        markup.add(join_button)
        markup.add(check_button)
        bot.send_message(
            message.chat.id,
            f"❗️ برای استفاده از این بات، ابتدا باید عضو کانال زیر شوید:\n@{CHANNEL_USERNAME}",
            reply_markup=markup
        )
        return

    if not can_user_request(user_id):
        bot.send_message(message.chat.id, "⚠️ شما به حد مجاز درخواست‌های امروز رسیده‌اید. لطفاً فردا دوباره امتحان کنید.")
        return

    if message.text == "💰 دریافت قیمت":
        bot.send_message(message.chat.id, "لطفاً نام ارز دیجیتال را وارد کنید:")
        bot.register_next_step_handler(message, get_price)
    elif message.text == "📉 تغییرات ۲۴ ساعته":
        bot.send_message(message.chat.id, "لطفاً نام ارز دیجیتال را وارد کنید:")
        bot.register_next_step_handler(message, get_24h)
    elif message.text == "🔔 تنظیم هشدار":
        bot.send_message(message.chat.id, "لطفاً نام ارز و قیمت هدف را وارد کنید (فرمت: bitcoin 50000):")
        bot.register_next_step_handler(message, set_price_alert)
    elif message.text == "📊 مقایسه ارزها":
        bot.send_message(message.chat.id, "لطفاً نام ارزهای دیجیتال را وارد کنید (با فاصله از هم جدا کنید):")
        bot.register_next_step_handler(message, compare_prices)
    elif message.text == "📰 اخبار ارزهای دیجیتال":
        get_news(message)
    elif message.text == "📈 نمودار قیمت":
        bot.send_message(message.chat.id, "لطفاً نام ارز دیجیتال را وارد کنید:")
        bot.register_next_step_handler(message, plot_price_chart)


#converting usd to irr

def get_usd_to_irr():
    try:
        response = requests.get(FIXER_URL)
        data = response.json()
        return data['rates']['IRR']
    except Exception as e:
        print(f"خطا در دریافت نرخ تبدیل دلار به ریال: {e}")
        return None


# def get_price(message):

def get_price(message):
    try:
        args = message.text.strip()
        args = convert_currency_name(args)
        params = {'ids': args, 'vs_currencies': 'usd'}
        response = requests.get(COINGECKO_URL, params=params)
        data = response.json()

        if args in data:
            price_usd = data[args]['usd']
            usd_to_ir = get_usd_to_irr()

            if usd_to_ir:
                price_ir = price_usd * usd_to_ir
                formatted_price_usd = "{:,.2f}".format(price_usd)
                formatted_price_ir = "{:,.0f}".format(price_ir)
                bot.reply_to(message, f"💵 قیمت {args}: {formatted_price_usd} دلار\n💰 معادل: {formatted_price_ir} تومان")
            else:
                bot.reply_to(message, f"💵 قیمت {args}: {formatted_price_usd} دلار\n⚠️ خطا در دریافت نرخ تبدیل به تومان.")
        else:
            bot.reply_to(message, "❌ ارز مورد نظر پیدا نشد. لطفاً دوباره امتحان کنید.")
    except Exception as e:
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره امتحان کنید.")
        print(f"خطا در دریافت قیمت: {e}")



#getting 24h update function

def get_24h(message):
    try:
        args = message.text.strip()
        args = convert_currency_name(args)
        url = f"https://api.coingecko.com/api/v3/coins/markets"
        params = {'vs_currency': 'usd', 'ids': args}
        response = requests.get(url, params=params)
        data = response.json()
        if len(data) > 0:
            change_24h = data[0]['price_change_percentage_24h']
            bot.reply_to(message, f"📈 تغییرات ۲۴ ساعته {args}: {change_24h:.2f}%")
        else:
            bot.reply_to(message, "❌ ارز مورد نظر پیدا نشد. لطفاً دوباره امتحان کنید.")
    except Exception as e:
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره امتحان کنید.")


#comparing prices function

def compare_prices(message):
    try:
        coins = message.text.strip().split()
        
        converted_coins = [convert_currency_name(coin) for coin in coins]

        params = {'ids': ','.join(converted_coins), 'vs_currencies': 'usd'}
        response = requests.get(COINGECKO_URL, params=params)
        data = response.json()

        comparison = ""
        for coin, original_name in zip(converted_coins, coins):
            if coin in data:
                price_usd = data[coin]['usd']
                usd_to_ir = get_usd_to_irr()
                
                if usd_to_ir:
                    price_ir = price_usd * usd_to_ir
                    
                    formatted_price_usd = "{:,.2f}".format(price_usd)
                    formatted_price_ir = "{:,.0f}".format(price_ir)

                    comparison += f"💵 قیمت {original_name}: {formatted_price_usd} دلار\n💰 معادل: {formatted_price_ir} تومان\n"
                else:
                    comparison += f"💵 قیمت {original_name}: {formatted_price_usd} دلار\n⚠️ خطا در دریافت نرخ تبدیل به تومان.\n"
            else:
                comparison += f"❌ ارز {original_name} پیدا نشد.\n"

        bot.reply_to(message, comparison)
        
    except Exception as e:
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره امتحان کنید.")


#setting alert function

alerts = {}

def set_price_alert(message):
    try:
        args = message.text.split()
        coin = convert_currency_name(args[0])
        target_price = float(args[1])
        user_id = message.chat.id

        if coin not in alerts:
            alerts[coin] = []

        alerts[coin].append({'user_id': user_id, 'target_price': target_price})
        bot.reply_to(message, f"🔔 هشدار قیمت {coin} در {target_price} دلار ثبت شد.")

    except Exception as e:
        bot.reply_to(message, "⚠️ فرمت دستور اشتباه است. لطفاً دوباره امتحان کنید.")


#getting news function

def get_news(message):
    try:
        url = f'https://newsapi.org/v2/everything?q=cryptocurrency&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'ok':
            articles = data['articles']
            news_text = "📰 آخرین اخبار ارزهای دیجیتال:\n\n"
            for article in articles[:5]:  #showing first 5 news
                title = article['title']
                url = article['url']
                news_text += f"📌 {title}\n🔗 [خواندن بیشتر]({url})\n\n"
            bot.reply_to(message, news_text, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ خبری یافت نشد.")
    except Exception as e:
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره امتحان کنید.")


#getting chart picture

def plot_price_chart(message):
    try:
        coin = convert_currency_name(message.text.strip())
        url = HISTORY_URL.format(coin)
        params = {'vs_currency': 'usd', 'days': '7'}
        response = requests.get(url, params=params)
        data = response.json()

        if 'prices' in data:
            prices = np.array(data['prices'])
            timestamps = prices[:, 0] / 1000
            values = prices[:, 1]

            plt.figure(figsize=(10, 5))
            plt.plot(timestamps, values, marker='o')
            plt.title(f'نمودار قیمت {coin} در ۷ روز گذشته')
            plt.xlabel('تاریخ')
            plt.ylabel('قیمت (دلار)')
            plt.xticks(rotation=45)
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()

            bot.send_photo(message.chat.id, photo=buf.getvalue())
        else:
            bot.reply_to(message, "❌ اطلاعات قیمت یافت نشد.")
    except Exception as e:
        bot.reply_to(message, "⚠️ خطایی رخ داد. لطفاً دوباره امتحان کنید.")
        print(f"خطا در تولید نمودار قیمت: {e}")
        
        

        
import time

while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=20, skip_pending=True)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)

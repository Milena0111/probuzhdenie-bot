import telebot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@yourchannel"
LEAD_MAGNET_FILE = "chek-list_marafon_OCR.pdf"

bot = telebot.TeleBot(TOKEN)

def check_subscription(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'creator', 'administrator']
    except Exception:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        if os.path.exists(LEAD_MAGNET_FILE):
            bot.send_message(user_id, "Спасибо за подписку! Вот твой подарок:")
            bot.send_document(user_id, open(LEAD_MAGNET_FILE, "rb"))
        else:
            bot.send_message(user_id, "Файл подарка не найден.")
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        btn = telebot.types.InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/yourchannel")
        markup.add(btn)
        bot.send_message(user_id, "Сначала подпишись на канал и нажми /start снова", reply_markup=markup)

bot.infinity_polling()

import os
import logging
from flask import Flask, request
import telebot

# Настройки
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8626271259:AAFEHyqGDcP3c0OtK3eCW_KV0KYRR7uxDW0")
SECRET = "qwerty123"
WEBHOOK_URL = f"https://striking-prosperity.up.railway.app/{SECRET}"

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём бота и Flask-приложение
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# Удаляем старый вебхук и устанавливаем новый
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
logger.info(f"Webhook set to {WEBHOOK_URL}")

# ------------------- ОСНОВНОЙ ОБРАБОТЧИК -------------------
@app.route('/' + SECRET, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "ok", 200
    else:
        return "Unsupported Media Type", 415

# Простой обработчик для проверки (чтобы браузер не ругался)
@app.route('/')
def hello():
    return "Бот работает!"

# ---------- ОБРАБОТЧИКИ КОМАНД БОТА ----------
@bot.message_handler(commands=['start'])
def simple_start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Бот работает на Railway!\n\n"
        "Я готов помогать с тренировками. Напиши /help для списка команд."
    )

@bot.message_handler(commands=['help'])
def simple_help(message):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n"
        "/start - приветствие\n"
        "/help - помощь\n"
        "Пока что я умею только это, но скоро добавлю новые функции!"
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

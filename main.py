import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "***"

# Функция для сокращения ссылки (через TinyURL)
def shorten_url(url: str) -> str:
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        return response.text if response.ok else "Ошибка при сокращении!"
    except Exception:
        return "Неверная ссылка!"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне ссылку, и я сокращу её через TinyURL."
    )

# Обработчик обычных сообщений (ссылок)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if user_text.startswith(("http://", "https://")):
        short_url = shorten_url(user_text)
        await update.message.reply_text(f"Сокращенная ссылка: {short_url}")
    else:
        await update.message.reply_text("Это не ссылка! Отправь URL, начинающийся с http:// или https://")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

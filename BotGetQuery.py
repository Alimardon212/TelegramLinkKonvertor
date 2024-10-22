import asyncio
from urllib.parse import unquote
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import urllib.parse

def extract_query_data(url):
    # URL'dan hash qismni olish (sharpy # dan keyingi qism)
    if '#' in url:
        hash_part = url.split('#')[1]  # '#' dan keyin keladigan qismni olish
    else:
        return "URL'da hash qism topilmadi."
    # tgWebAppData ni ajratish
    if 'tgWebAppData=' in hash_part:
        # tgWebAppData dan keyingi qismni ajratish
        query_string = hash_part.split('tgWebAppData=')[1]
    else:
        return "tgWebAppData qismi topilmadi."
    # URL parametrlarini ajratib olish
    query_string = urllib.parse.unquote(query_string)  # Avval dekodlash
    query_params = query_string.split('&')  # '&' orqali ajratamiz
    params_dict = {}
    for param in query_params:
        if '=' in param:
            key, value = param.split('=', 1)  # faqat birinchi '=' dan ajratish
            params_dict[key] = value
    # query_id, user, auth_date va hash ni ajratib olish
    query_id = params_dict.get('query_id')
    user = params_dict.get('user')
    auth_date = params_dict.get('auth_date')
    hash_value = params_dict.get('hash')
    if query_id and user and auth_date and hash_value:
        result = (
            f"query_id={query_id}&"
            f"user={user}&"
            f"auth_date={auth_date}&"
            f"hash={hash_value}"
        )
        return result
    else:
        return f"Kerakli parametrlar topilmadi. query_id: {query_id}, user: {user}, auth_date: {auth_date}, hash: {hash_value}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Salom! URL jo\'natishingiz mumkin.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    if user_message.startswith('http://') or user_message.startswith('https://'):
        await update.message.reply_text(f"```{extract_query_data(user_message)}```", parse_mode="Markdown")
async def main() -> None:
    # Bot tokenini fayldan o'qish
    with open('YOUR_BOT_TOKEN.txt', 'r') as token_file:
        token = token_file.read().strip()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot ishga tushdi...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    try:
        while True:
            await asyncio.sleep(1)  # Bu botni doimiy ishlatadi
    finally:
        await app.stop()  # Ilovani to'xtatish

if __name__ == '__main__':
    asyncio.run(main())  # O'rnatilgan asyncio.run() yordamida ishga tushirish

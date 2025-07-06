import os
import csv
import requests
from io import StringIO
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# التوكن من متغير البيئة
TOKEN = os.getenv("BOT_TOKEN")  # تم جلب التوكن من متغير البيئة

# رابط تحميل ملف البيانات من Google Drive
DATA_URL = "https://drive.google.com/uc?export=download&id=1tgAg9mGDCzBkK3PCkTp4jzZ3hsS5UeY1"

def download_data():
    response = requests.get(DATA_URL)
    response.raise_for_status()
    text = response.content.decode('utf-8', errors='ignore')
    return text

def search_in_data(data_text, query):
    results = []
    csvfile = StringIO(data_text)
    reader = csv.reader(csvfile)
    for row in reader:
        if any(query.lower() in (field or '').lower() for field in row):
            results.append(', '.join(row))
    return results

def start(update: Update, context: CallbackContext):
    update.message.reply_text("أرسل رقم أو اسم للبحث عنه.")

def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    data_text = download_data()
    results = search_in_data(data_text, query)
    if results:
        update.message.reply_text('\n\n'.join(results[:10]))
    else:
        update.message.reply_text("لا توجد نتائج.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

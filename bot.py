import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = '7765655149:AAGe_fTFLqlS7NHp6a9-VaBCRd5foe8-JNA'  # ваш токен

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите ссылку на товар Wildberries.')

async def get_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0] if context.args else None
    if not url:
        await update.message.reply_text('Пожалуйста, введите ссылку на товар.')
        return

    product_id = extract_product_id(url)
    if not product_id:
        await update.message.reply_text('Не удалось извлечь ID товара. Убедитесь, что ссылка корректна.')
        return

    images = extract_product_images(product_id)
    if not images:
        await update.message.reply_text('Не удалось найти изображения товара.')
        return

    await update.message.reply_text(f'ID товара: {product_id}')
    for img in images:
        await update.message.reply_photo(img)

def extract_product_id(url):
    # Извлечение ID из ссылки
    try:
        return url.split('/')[-2]  # ID перед последним слэшем
    except IndexError:
        return None

def extract_product_images(product_id):
    product_id = int(product_id)
    images = []
    vol = int(product_id / 100000)
    part = int(product_id / 1000)
    host = ''
    if (vol >= 0 and vol <= 143):
        host = '01'
    elif (vol >= 144 and vol <= 287):
        host = '02'
    elif (vol >= 288 and vol <= 431):
        host = '03'
    elif (vol >= 432 and vol <= 719):
        host = '04'
    elif (vol >= 720 and vol <= 1007):
        host = '05'
    elif (vol >= 1008 and vol <= 1061):
        host = '06'
    elif (vol >= 1062 and vol <= 1115):
        host = '07'
    elif (vol >= 1116 and vol <= 1169):
        host = '08'
    elif (vol >= 1170 and vol <= 1313):
        host = '09'
    elif (vol >= 1314 and vol <= 1601):
        host = '10'
    elif (vol >= 1602 and vol <= 1655):
        host = '11'
    elif (vol >= 1656 and vol <= 1919):
        host = '12'
    elif (vol >= 1920 and vol <= 2045):
        host = '13'
    elif (vol >= 1920 and vol <= 2189):
        host = '14'
    elif (vol >= 1920 and vol <= 2405):
        host = '15'
    elif (vol >= 1920 and vol <= 2621):
        host = '16'
    elif (vol >= 1920 and vol <= 2837):
        host = '17'
    else:
        host = '18'
    for nm in range(10):
        images.append(f'https://basket-{host}.wbbasket.ru/vol{vol}/part{part}/{product_id}/images/big/{nm+1}.webp')

    return images

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_product", get_product))
    
    app.run_polling()

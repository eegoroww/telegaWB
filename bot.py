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
    # Получение страницы товара
    response = requests.get(f'https://www.wildberries.ru/catalog/{product_id}/detail.aspx')
    if response.status_code != 200:
        return None

    # Анализ HTML-кода страницы
    soup = BeautifulSoup(response.content, 'html.parser')
    images = []

    # Поиск изображений
    for img in soup.select('img[data-test-id="main-image"]'):
        images.append(img['src'])

    return images

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get_product", get_product))
    
    app.run_polling()

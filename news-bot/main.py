# Import necessary libraries
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink
from celery import Celery
from aiohttp import web
import json
from scraping_news import get_euro, get_football, get_uzb
import asyncio

# Telegram API Token
TOKEN_API = '6322573292:AAFEFo68GPPbzqOHQVEduL5oZ7l5K-QxhIo'
bot = Bot(TOKEN_API, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
app = web.Application()

webhook_path = f'/{TOKEN_API}'

async def set_webhook():
    webhook_uri = f'https://8a13-213-230-116-150.ngrok-free.app{webhook_path}'
    await bot.set_webhook(webhook_uri)
    
    
async def on_startup(_):
    await set_webhook()
    print('Бот был успешно запушен!')

async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index+1:]
    
    if token == TOKEN_API:
        update = types.Update(**await request.jon())
        await dp.process_update(update)
        
        return web.Response()
    
    else:
        return web.Response(status=403)

app.router.add_post(f'/{TOKEN_API}', handle_webhook)


# Celery configuration
app_celery = Celery('tasks', broker='redis://localhost:6379/0')

# Command constants
HELP_COMMAND = "/help - список команд\n/start - начат работу с ботом"
   
# Celery task for sending scheduled messages
@app_celery.task
async def send_scheduled_message(chat_id, text, delay):
    await asyncio.sleep(delay)
    await bot.send_message(chat_id, text)

# Callback function to handle /help command
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)

# Callback function to handle /start command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    start_buttons = ["Futbol yangiliklari ⚽️", "Jaxon yangiliklari 🏆", "Maxalliy yangiliklar 🇺🇿", "Avtomatik qabul qilish 🕰"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(text="<b>Добро пожаловать в наш Телеграмм бот!</b>", 
                         parse_mode="HTML",
                         reply_markup=keyboard)
    print(f'{message.chat.full_name} + {message.text}')
    await message.delete()
    
    
# Callback function to handle  command
@dp.message_handler(Text(equals="Futbol yangiliklari ⚽️"))
async def get_football_news(message:types.Message):
    await message.answer("Iltimos kuting...")
    get_football()
    with open("data/football.json",encoding="utf-8") as file:
        data = json.load(file)
    for item in data[:5]:
        card = f"{hlink(item.get('title'), item.get('url'))}\n "
        await message.answer(card)
        
        
# Callback function to handle  command
@dp.message_handler(Text(equals="Maxalliy yangiliklar 🇺🇿"))
async def get_uzb_news(message:types.Message):
    await message.answer("Iltimos kuting...")
    get_uzb()
    with open("data/uzb.json",encoding="utf-8") as file:
        data = json.load(file)
    for item in data[:5]:
        card = f"{hlink(item.get('title'), item.get('url'))}\n "
        await message.answer(card)
        
        
# Callback function to handle  command       
@dp.message_handler(Text(equals="Jaxon yangiliklari 🏆"))
async def get_euro_news(message:types.Message):
    await bot.send_message(message.from_user.id, "Start!")
    await message.answer("Iltimos kuting...")
    get_euro()
    with open("data/euro.json",encoding="utf-8") as file:
        data = json.load(file)
    for item in data[:5]:
        card = f"{hlink(item.get('title'), item.get('url'))}\n "
        await message.answer(card)

# Callback function to schedule a message after /schedule command
@dp.message_handler(Text(equals='Avtomatik qabul qilish 🕰'))
async def schedule(message: types.Message):
    chat_id = message.chat.id
    text = "Your scheduled message"
    delay = 15 # 5 seconds delay (adjust as needed)
    await get_euro_news(message)
    await get_uzb_news(message)
    await get_football_news(message)
    await bot.send_message(chat_id=chat_id, text=f"Sizga har {delay} sekundda habarlarni avtomatik jo\'natiladi!.")

    while True:
        await asyncio.sleep(delay)
        await bot.send_message(chat_id, text)

# Start the bot


if __name__ == '__main__':
    # executor.start_polling(dp, on_startup=on_startup,skip_updates=True)
    app.on_startup.append(on_startup)
    
    web.run_app(
        app,
        host='0.0.0.0',
        port=8080
    )
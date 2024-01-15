from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink
from scraping_news import get_football, get_uzb, get_euro
import json, time
from celery import Celery
from datetime import datetime, timedelta
import schedule

TOKEN_API = '6322573292:AAFEFo68GPPbzqOHQVEduL5oZ7l5K-QxhIo'

HELP_COMMAND = """
/help - список команд
/start - начат работу с ботом"""

app = Celery('tasks', broker='redis://localhost:6379/0')
bot = Bot(TOKEN_API, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

async def on_startup(_):
    # schedule_messages()
    print('Бот был успешно запушен!')
    schedul()



@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    start_buttons = ["Futbol yangiliklari ⚽️", "Jaxon yangiliklari 🏆", "Maxalliy yangiliklar 🇺🇿"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(text="<b>Добро пожаловать в наш Телеграмм бот!</b>", 
                         parse_mode="HTML",
                         reply_markup=keyboard)
    await message.delete()
    print(message)
    
    
@dp.message_handler(Text(equals="Futbol yangiliklari ⚽️"))
async def get_football_news(message:types.Message):
    await message.answer("Iltimos kuting...")
    
    get_football()
    
    with open("data/football.json",encoding="utf-8") as file:
        data = json.load(file)
        
    for item in data[:5]:
        card = f"{hlink(item.get('title'), item.get('url'))}\n "

        await message.answer(card)
        
@dp.message_handler(Text(equals="Maxalliy yangiliklar 🇺🇿"))
async def get_uzb_news(message:types.Message):
    await message.answer("Iltimos kuting...")
    
    get_uzb()
    
    with open("data/uzb.json",encoding="utf-8") as file:
        data = json.load(file)
        
    for item in data[:5]:
        card = f"{hlink(item.get('title'), item.get('url'))}\n "

        await message.answer(card)
        
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

@app.task
def send_message():
    chat_id = '1690731346'
    message = 'YOUR_MESSAGE_HERE'
    bot.send_message(chat_id=chat_id, text=message)
def schedul():    
    schedule.every(3).seconds.do(send_message.delay)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
    
# @app.task
# def schedule_messages():
#     print('redis working!')
#     send_message.apply_async(eta=datetime.now() + timedelta(seconds=10))
#     send_message.apply_async(eta=datetime.now() + timedelta(hours=7, seconds=10))

    
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup,skip_updates=True)

    
    
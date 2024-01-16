from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink
from scraping_news import get_football, get_uzb, get_euro
import json
from celery import Celery
from datetime import datetime, timedelta
import time
import asyncio

TOKEN_API = '6322573292:AAFEFo68GPPbzqOHQVEduL5oZ7l5K-QxhIo'

HELP_COMMAND = """
/help - список команд
/start - начат работу с ботом"""

app = Celery('tasks', broker='redis://localhost:6379/0')
bot = Bot(TOKEN_API, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Бот был успешно запушен!')



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
    

# Определение задачи Celery
@app.task
def send_scheduled_message(chat_id, text, delay):
    asyncio.run(schedule_message(chat_id, text, delay))


# Отправка запланированного сообщения
async def schedule_message(chat_id, text, delay):
    await asyncio.sleep(delay)
    await bot.send_message(chat_id, text)
    
    
# Обработчик команды /schedule
@dp.message_handler(commands=['schedule'])
async def schedule(message: types.Message):
    chat_id = message.chat.id
    text = "Your scheduled message"
    print(1)
    delay = 5  # 5 minutes delay (in seconds)
    # send_scheduled_message.apply_async((chat_id, text, delay))
    await bot.send_message(chat_id=chat_id, text=text)
    send_scheduled_message.apply_async((chat_id, text, delay), countdown=delay)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup,skip_updates=True)
    

    
    
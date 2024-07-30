import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types


API_TOKEN = 'YOUR TELEGRAM TOKEN'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

async def on_startup(dp):
    print('Bot is starting...')

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to the Flower Delivery Bot!")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Send your flower order details and we'll process it.")

@dp.message_handler()
async def handle_order(message: types.Message):
    # Here you would add the code to handle orders, e.g., save to database
    await message.reply("Order received! We will process it soon.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

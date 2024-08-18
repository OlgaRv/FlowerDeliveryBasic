from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# Ваш токен бота
bot_token = '7398031401:AAGb1uvxXNOOa8JacOnuNSqcCKx1BdjRiJI'

# Создаем объект бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(f"Your chat ID is {message.chat.id}")

async def main():
    # Запуск поллинга
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


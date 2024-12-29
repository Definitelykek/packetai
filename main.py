from text import welcome
from aiogram import Bot, Dispatcher
from openai import AsyncOpenAI
from dotenv import load_dotenv
from aiogram.filters import Command
from database.models import async_main
import asyncio
import os
from app.handlers import router





# Загружаем файлы из .env
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message):
    await message.answer(welcome)


# Диспетчер начинает проверять бот
async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)

#Запуск только во время файла
if __name__ == '__main__':
   try:
       asyncio.run(main())
   except:
       print("Загрузка")



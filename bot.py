import asyncio
from aiogram import Bot, Dispatcher
from handlers import start

TOKEN = '7805066697:AAEQqN7tBOT4sXUdK5c4Gz3M61-1TXY5C30'

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(start.router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

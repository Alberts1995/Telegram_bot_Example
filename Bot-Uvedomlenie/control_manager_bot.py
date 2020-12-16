import logging
from aiogram import Bot, Dispatcher, executor, types
from config import token_asinc
from Task_manager_bd import SQLite
import asyncio



bd = SQLite()

logging.basicConfig(level=logging.INFO)


bot = Bot(token_asinc)
dp = Dispatcher(bot)


@dp.message_handler(commands = ["start"])
async def echo(message: types.Message):
    while True:
        bd_info = (bd.select_all_for_asinck_bot())
        for x in bd_info:
            await bot.send_message(int([x][0][0]), "Задание: "+  [x][0][1])
            await asyncio.sleep([x][0][2])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    
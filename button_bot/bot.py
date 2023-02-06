from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет\nЗдорово!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("just echo everything, except commands")

@dp.message_handler()
async def echo_msg(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)

def run_echo_bot():

    executor.start_polling(dp)

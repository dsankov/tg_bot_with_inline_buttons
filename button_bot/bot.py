from random import randint
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import logging
from typing import Optional, Union
from contextlib import suppress
from aiogram.utils.exceptions import BadRequest

from aiogram.utils.exceptions import MessageNotModified


from icecream import ic

from config import TOKEN
from button_bot.keyboards.reversi_board import get_game_board
from button_bot.callback_datas import cell_CallbackData
from button_bot.callback_datas import game_board



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

user_data = {}




def run_echo_bot():
    executor.start_polling(dp)
    




@dp.message_handler(commands=["board"])
async def process_board_command(message: types.Message):
    await message.answer("board test", reply_markup=get_game_board())

@dp.callback_query_handler(cell_CallbackData.filter())
async def process_cell_pressed(callback_query: types.CallbackQuery, callback_data: dict):
    
    y = callback_data['y']
    x = callback_data['x']
    ic(callback_data)
    game_board[int(y)][int(x)] = 1
    
    await callback_query.message.edit_text(
        text=f"pressed cell: {y}, {x}",
        reply_markup=get_game_board()
        )

    await callback_query.answer()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("/help\n/board")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer(
        text="echo everything\nUse commands for more", 
        reply_markup=types.ReplyKeyboardRemove()
        )

@dp.message_handler()
async def echo_msg(message: types.Message):
    ic(message.text)
    await bot.send_message(message.from_user.id, message.text)

@dp.errors_handler(exception=MessageNotModified)
async def board_not_modified_handler(update, error):
    return True


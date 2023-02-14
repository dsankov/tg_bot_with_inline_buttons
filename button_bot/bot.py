from random import randint
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import logging
from typing import Optional, Union
from contextlib import suppress
from aiogram.utils.exceptions import BadRequest
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified


from icecream import ic

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

user_data = {}
WHITE_CIRCLE = '\u25ef'     # ◯
BLACK_CIRCLE = '\u2b24'     # ⬤ 
NUMS_IN_CIRCLE = {0:9450, 1:9312, 2:9313, 3:9314, 4:9315, 5:9316, 6:9317, 7:9318, 8:9319, 9:9320,
                  10:9321, 11:9322, 12:9323, 13:9324, 14:9325, 15:9326, 16:9327, 17:9328, 18:9329, 19:9330
                  }
game_board = [[0]*8 for _ in range(8)]
game_board[3][3], game_board[4][4] = 1, 1
game_board[3][4], game_board[4][3] = -1, -1
game_board[0][0] = 2
game_board[0][1] = 3
game_board[0][2] = 18

cell_CallbackData = CallbackData("cell", "y", "x")


def get_game_board():
    board_markup = types.InlineKeyboardMarkup(row_width=3)
    for y in range(8):
        row_markup = []
        for x in range(8):
            if game_board[y][x] == 1:
                cell_text = WHITE_CIRCLE 
            elif game_board[y][x] == -1:
                cell_text = BLACK_CIRCLE 
            elif game_board[y][x] == 0:
                cell_text = '\u2003' # space
            else:
                cell_text = chr(NUMS_IN_CIRCLE[game_board[y][x]])

            cell_coord = 'cell:' + str(y) + ':' + str(x)
            row_markup.append(
                types.InlineKeyboardButton(
                    cell_text, 
                    callback_data=cell_CallbackData.new(y=y, x=x)
                    )
                )

        board_markup.row(*row_markup)

    return board_markup



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

@dp.errors_handler(exception=MessageNotModified)
async def board_not_modified_handler(update, error):
    return True





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

def run_echo_bot():
    executor.start_polling(dp)

from random import randint
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import logging
from typing import Optional, Union
from contextlib import suppress
from aiogram.utils.exceptions import BadRequest



from icecream import ic

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

user_data = {}
game_board = [[0]*8 for _ in range(8)]
game_board[3][3], game_board[4][4] = 1, 1
game_board[3][4], game_board[4][3] = -1, -1
game_board[0][0] = 11
game_board[7][7] = 12

def get_game_board():
    board_markup = types.InlineKeyboardMarkup(row_width=3)
    for i in range(8):
        row_markup = []
        for j in range(8):
            if game_board[i][j] == 1:
                cell_text = '\u25ef' # ◯
            elif game_board[i][j] == -1:
                cell_text = '\u2b24' #🔴
            elif game_board[i][j] == 0:
                cell_text = '\u2003' # space
            elif game_board[i][j] == 11:
                cell_text = '\u2461' # space
            elif game_board[i][j] == 12:
                cell_text = '\u2471' # space
                
            cell_coord = 'cell:' + str(i) + ':' + str(j)
            row_markup.append(types.InlineKeyboardButton(cell_text, callback_data=cell_coord))

        board_markup.row(*row_markup)

    return board_markup


@dp.message_handler(commands=["board"])
async def process_board_command(message: types.Message):
    await message.answer("board test", reply_markup=get_game_board())

@dp.callback_query_handler(Text(startswith="cell"))
async def process_cell_pressed(callback_query: types.CallbackQuery):
    
    _, y, x = callback_query.data.split(':')
    ic(y,x)
    game_board[int(y)][int(x)] = 1
    
    with suppress(BadRequest):
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

def run_echo_bot():
    executor.start_polling(dp)

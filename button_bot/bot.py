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


@dp.message_handler(commands=['333'])
async def process_board_command(message: types.Message):
    await message.answer("board test", reply_markup=get_game_board())

@dp.callback_query_handler(Text(startswith="cell"))
async def process_cell_pressed(callback_query: types.CallbackQuery):
    _, y, x = callback_query.data.split(':')
    ic(y,x)
    game_board[int(y)][int(x)] = 1
    await callback_query.message.edit_text(f"pressed cell: {y}, {x}",reply_markup=get_game_board())
    await callback_query.answer()




def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
        ],
        [types.InlineKeyboardButton(text="OK", callback_data="num_finish")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def update_num_text(message: types.Message, new_value: int):
    with suppress(BadRequest):
        await message.edit_text(
            f"Укажтите число: {new_value}",
            reply_markup=get_keyboard()
        )

@dp.message_handler(commands=['22'])
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())

@dp.callback_query_handler(Text(startswith="num_"))
async def callback_nums(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value + 1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value - 1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")
    
    await callback.answer()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет\nЗдорово!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer("just echo everything, except commands", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['reply_kb'])
async def process_kbbuttons_command(message: types.Message):
    custom_kb = [
        [
            types.KeyboardButton(text="первый"),
            types.KeyboardButton(text="второй"),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=custom_kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери вариант",
        )

    await message.answer(text="какой?", reply_markup=keyboard)

@dp.message_handler(commands=['11'])  
@dp.message_handler(commands=['inline_kb'])  
async def process_inline_kb_buttons(message: types.Message):
    inline_kb_btn1 = types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value"
        )
    inline_kb1 = types.InlineKeyboardMarkup().add(inline_kb_btn1)

    await message.answer(
        text="inline button expected",
        reply_markup=inline_kb1
    )

@dp.callback_query_handler(text='random_value')
async def random_value(callback: types.CallbackQuery):
     await callback.message.answer(str(randint(1, 10)))

     await callback.answer()





@dp.message_handler()
async def echo_msg(message: types.Message):
    ic(message.text)
    await bot.send_message(message.from_user.id, message.text)

def run_echo_bot():

    executor.start_polling(dp)

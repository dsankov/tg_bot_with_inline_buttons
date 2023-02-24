
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import MessageNotModified

from icecream import ic

from button_bot.keyboards.reversi_board import get_game_board


def register_commands_handlers(dp: Dispatcher):
    ic("dispatcher started", dp)
    dp.register_message_handler(process_board_command, commands=["board"])
    dp.register_message_handler(process_start_command, commands=["start"])
    dp.register_message_handler(process_help_command, commands=["help"])
    
    dp.register_message_handler(echo_msg)
    dp.register_errors_handler(board_not_modified_handler, exception=MessageNotModified)


async def process_board_command(message: types.Message):

    await message.answer("board test", reply_markup=get_game_board())

async def echo_msg(message: types.Message):
    ic(message.text)
    await message.answer(message.text)

async def process_start_command(message: types.Message):
    await message.answer("/help\n/board")

async def process_help_command(message: types.Message):
    await message.answer(
        text="echo everything\nUse commands for more", 
        reply_markup=types.ReplyKeyboardRemove()
        )
# @dp.errors_handler(exception=MessageNotModified)
async def board_not_modified_handler(update, error):
    return True
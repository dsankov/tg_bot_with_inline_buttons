from log2d import Log
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Dispatcher,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)    
from button_bot.keyboards.reversi_board import build_initial_game_markup

log = Log("handlers").logger


def set_commands_handlers(dispatcher: Dispatcher):
    start_command_handler = CommandHandler(
        command="start", 
        callback=process_start_command
        )
    dispatcher.add_handler(start_command_handler)
    
    help_command_handler = CommandHandler(
        command="help", 
        callback=process_help_command
        )
    dispatcher.add_handler(help_command_handler)
    
    board_command_handler = CommandHandler(
        command="board", 
        callback=process_board_command
        )
    dispatcher.add_handler(board_command_handler)

    unknown_command_handler = MessageHandler(
        filters=Filters.command,
        callback=process_unknown_command
        )
    dispatcher.add_handler(unknown_command_handler)

def set_message_handlers(dispatcher: Dispatcher):
    echo_handler = MessageHandler(
        filters=Filters.text & (~Filters.command), 
        callback=echo_message
        )
    dispatcher.add_handler(echo_handler)
    
def echo_message(update: Update, context: CallbackContext):
    """
    echoes non commands text messages
    """
    log.info(f"message {update.message.text} received")
    echo_text = "echo: " + update.message.text
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = echo_text
    )
 
def process_start_command(update: Update, context: CallbackContext):
    log.info("/start command received")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="trying to start the bot over"
    )
    
def process_help_command(update: Update, context: CallbackContext):
    log.info("/help command received")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="use /start to start the bot over\nuse /board to play reversi game"
    )
    
def process_board_command(update: Update, context: CallbackContext):
    log.info("/board command received")
    initial_game_markup = build_initial_game_markup()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="game started",
        reply_markup=initial_game_markup
    )
    

    
def process_unknown_command(update: Update, context: CallbackContext):
    log.info(f"unknown command {update.message.text} received")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"command {update.message.text} not recognised"
    )
    


# from aiogram import types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils.exceptions import MessageNotModified

# from icecream import ic

# from button_bot.keyboards.reversi_board import get_game_board


# def register_commands_handlers(dp: Dispatcher):
#     ic("dispatcher started", dp)
#     dp.register_message_handler(process_board_command, commands=["board"])
#     dp.register_message_handler(process_start_command, commands=["start"])
#     dp.register_message_handler(process_help_command, commands=["help"])
    
#     dp.register_message_handler(echo_msg)
#     dp.register_errors_handler(board_not_modified_handler, exception=MessageNotModified)


# async def process_board_command(message: types.Message):

#     await message.answer("board test", reply_markup=get_game_board())

# async def echo_msg(message: types.Message):
#     ic(message.text)
#     await message.answer(message.text)

# async def process_start_command(message: types.Message):
#     await message.answer("/help\n/board")

# async def process_help_command(message: types.Message):
#     await message.answer(
#         text="echo everything\nUse commands for more", 
#         reply_markup=types.ReplyKeyboardRemove()
#         )

# async def board_not_modified_handler(update, error):
#     return True
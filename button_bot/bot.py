from config import TOKEN
from log2d import Log
from telegram import (
    BotCommand, 
    
)
from telegram.ext import (
    Updater,
    Dispatcher, 

)
from button_bot.handlers.message_handlers import (
    set_commands_handlers,
    set_message_handlers,
)
from button_bot.handlers.callback_handlers import set_callback_handlers

log = Log("bot").logger
    
def run_echo_bot():

    log.info("bot started")
    updater :Updater = Updater(token=TOKEN)
    dispatcher :Dispatcher = updater.dispatcher
    log.info(f"Updater & Dispatcher objects created")
    
    set_bot_commands(updater=updater)
    set_commands_handlers(dispatcher=dispatcher)
    set_message_handlers(dispatcher)
    set_callback_handlers(dispatcher)

    updater.start_polling()
    log.info("updeter polling started")
    updater.idle()
    log.info("bot stopped")
    
def set_bot_commands(updater: Updater):
    """
    register pre-defined bot commands from list bellow
    """
    
    bot_commands = {
        "start":    "start bot",
        "help":     "get help",
        "board":    "start reversi game"
    }
    bot_commands_list = [
        BotCommand(command=cmd, description=desc) 
            for (cmd, desc) in bot_commands.items()
        ]
    updater.bot.set_my_commands(bot_commands_list)    
    log.info(f"bot commands set up: {list(bot_commands.keys())}")
    
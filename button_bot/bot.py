
#from typing import Optional, Union

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
#from aiogram.dispatcher.filters import Text
#from aiogram.utils.exceptions import BadRequest, MessageNotModified
from icecream import ic

#from button_bot.callback_datas import cell_CallbackData, game_board
from button_bot.handlers.message_handlers import register_commands_handlers
from button_bot.handlers.callback_handlers import register_callback_handlers
from config import TOKEN

# logging.basicConfig(level=logging.INFO)


async def run_echo_bot():
    bot = Bot(token=TOKEN)
    
    dp = Dispatcher(bot)
    await set_default_commands(dp)
    register_commands_handlers(dp)
    register_callback_handlers(dp)
    
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close() 


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("board", "Доска"),
    ])


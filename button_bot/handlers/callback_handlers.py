from log2d import Log
from telegram import (
    Update,
)

from telegram.ext import (
    Dispatcher,
    CallbackQueryHandler,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)   

from button_bot.keyboards.reversi_keyboard import build_initial_game_markup
 
log = Log("call_handlers").logger


def set_callback_handlers(dispatcher: Dispatcher):
    board_cell_handler = CallbackQueryHandler(callback=process_cell_button)
    dispatcher.add_handler(board_cell_handler)
    log.info("cell button handler registred")

def process_cell_button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    log.info(f"data {data} received")
    query.answer()
    
    
    initial_game_markup = build_initial_game_markup()
    query.edit_message_text(text=f"{data}",reply_markup=initial_game_markup)

    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=f"{data}",
    #     reply_markup=initial_game_markup
    # )
    # query.edit_message_reply_markup(reply_markup=initial_game_markup)
    
 
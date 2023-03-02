from log2d import Log
from telegram import (
    Update,
)
from typing import List

from telegram.ext import (
    Dispatcher,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
)   

from button_bot.keyboards.reversi_keyboard import (
    build_initial_game_markup,
    build_game_markup,
)
from button_bot.games.reversi_game import reversi_game, reversi_player
 
log = Log("call_handlers").logger

INIT_STATE, BLACK_MOVE, WHITE_MOVE, GAME_FINISHED = range(4)

def process_board_command(update: Update, context: CallbackContext):
    log.info("/board command received")
    initial_game_markup = build_initial_game_markup()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="game started, black move first\nnext move: black",
        reply_markup=initial_game_markup
    )
    return BLACK_MOVE

def unpack_context(data: str) -> tuple[str, tuple[int, int]]:
    cell_mark, y, x = data.split(":")
    return [cell_mark, [int(y), int(x)]]
    

def process_black_move_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    mark, position = unpack_context(data)
    y, x = position
    log.info(f"black move at x={x} y={y} received")
    
    reversi_game.make_move(reversi_player.BLACK, position)
    game_markup = build_game_markup()
    query.edit_message_text(text=f"black move at x={x+1} y={y+1}\nnext move: white",reply_markup=game_markup)

    return WHITE_MOVE

def process_white_move_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    mark, position = unpack_context(data)
    y, x = position
    log.info(f"white move at x={x} y={y} received")
    
    reversi_game.make_move(reversi_player.WHITE, position)    
    game_markup = build_game_markup()
    query.edit_message_text(text=f"white move at x{x+1} y={y+1}\nnext move: black",reply_markup=game_markup)
    
    return BLACK_MOVE

def process_not_empty_cell(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    mark, position = unpack_context(data)
    y, x = position
    log.info(f"click at x={x} y={y} received")
    
    game_markup = build_game_markup()
    query.edit_message_text(text=f"cell at x={x+1} y={y+1} not empty\ntry anain",
                            reply_markup=game_markup
                            )
    
def stop_handler(update: Update, context: CallbackContext):
    log.info("stop command")
    return ConversationHandler.END


def set_callback_handlers(dispatcher: Dispatcher):

    board_command_handler = CommandHandler(
        command="board", 
        callback=process_board_command
        )
    
    game_handler = ConversationHandler(
        entry_points=[board_command_handler],
        states={
            BLACK_MOVE: [
                CallbackQueryHandler(process_black_move_button, pattern="^e"),
                CallbackQueryHandler(process_not_empty_cell, pattern="^(b|w)")
            ],
            WHITE_MOVE: [
                CallbackQueryHandler(process_white_move_button, pattern="^e"),
                CallbackQueryHandler(process_not_empty_cell, pattern="^(b|w)")
            ],
            GAME_FINISHED: [
                CallbackQueryHandler(process_black_move_button),
            ],
        },
        fallbacks=[
            board_command_handler,
            CommandHandler("stop", stop_handler),
        ]
    )
    dispatcher.add_handler(game_handler)
    log.info("game handler registred")
    
    
    
    
 
    # context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text=f"{data}",
    #     reply_markup=initial_game_markup
    # )
    # query.edit_message_reply_markup(reply_markup=initial_game_markup)
    
 
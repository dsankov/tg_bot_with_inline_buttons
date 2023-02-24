from log2d import Log
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

log = Log("keybd").logger

BOARD_SIZE = 8
WHITE_CIRCLE = '\u25ef'     # ◯
BLACK_CIRCLE = ' \u2b24 '     # ⬤ 

def build_initial_game_markup(header_buttons=None, footer_buttons=None):
    """
    header_ and footer_buttons: List[List[InlineKeyboardButton]]
    so may be multiline
    """
    
    menu = []
    if not header_buttons:
        header_buttons = get_default_header_buttons()
    menu.extend(header_buttons)
    
    game_board = get_game_board()
    menu.extend(game_board)
    
    if not footer_buttons:
        footer_buttons = get_default_footer_buttons()
    menu.extend(footer_buttons)

    log.info("initial game menu constructed")
    return InlineKeyboardMarkup(menu)

def get_default_header_buttons():
    return []

def get_default_footer_buttons():
    footer_buttons = [
        [InlineKeyboardButton("col1", callback_data="1.1"), InlineKeyboardButton("col2", callback_data="1.2")],
        [InlineKeyboardButton("row 2", callback_data="2.0")]
    ]
    return footer_buttons

def get_game_board():
    board = []
    for y in range(BOARD_SIZE):
        row = []
        for x in range(BOARD_SIZE):
            row.append(InlineKeyboardButton(
                text=BLACK_CIRCLE,
                callback_data=f"cell:{y}:{x}"
                )
                       )
        board.append(row)
    return board
    




# NUMS_IN_CIRCLE = {0:9450, 1:9312, 2:9313, 3:9314, 4:9315, 5:9316, 6:9317, 7:9318, 8:9319, 9:9320,
#                   10:9321, 11:9322, 12:9323, 13:9324, 14:9325, 15:9326, 16:9327, 17:9328, 18:9329, 19:9330
#                   }


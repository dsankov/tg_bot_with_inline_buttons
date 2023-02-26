from log2d import Log
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

log = Log("keybd").logger

BOARD_SIZE = 8
WHITE_BUTTON = '\u25ef'     # ◯
BLACK_BUTTON = ' \u2b24 '     # ⬤ 
EMPTY_BUTTON = "."


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

CELL_EMPTY = 0
CELL_BLACK = -1
CELL_WHITE = -2

def get_game_board():
    board_state = get_board()
    board_size = len(board_state)
    board = []
    for y in range(board_size):
        row = []
        for x in range(board_size):
            if board_state[y][x] == CELL_EMPTY:
                cell_text = EMPTY_BUTTON
                cell_data = f"e:{y}:{x}"
            elif board_state[y][x] == CELL_BLACK:        
                cell_text = BLACK_BUTTON
                cell_data = f"b:{y}:{x}"
            elif board_state[y][x] == CELL_WHITE:        
                cell_text = WHITE_BUTTON
                cell_data = f"w:{y}:{x}"
            else:     
                cell_text = "?"
                cell_data = f"e:{y}:{x}"
            
            cell_button = InlineKeyboardButton(text=cell_text, callback_data=cell_data)
            row.append(cell_button)
        board.append(row)
    return board
    
def get_board():
    board = [[CELL_EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[3][4], board[4][3] = CELL_BLACK, CELL_BLACK
    board[3][3], board[4][4] = CELL_WHITE, CELL_WHITE
    board[7][7] = 4
    return board



# NUMS_IN_CIRCLE = {0:9450, 1:9312, 2:9313, 3:9314, 4:9315, 5:9316, 6:9317, 7:9318, 8:9319, 9:9320,
#                   10:9321, 11:9322, 12:9323, 13:9324, 14:9325, 15:9326, 16:9327, 17:9328, 18:9329, 19:9330
#                   }


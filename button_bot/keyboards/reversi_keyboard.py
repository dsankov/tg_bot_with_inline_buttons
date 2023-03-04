from log2d import Log
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    
)
from button_bot.games.reversi_game import (
    reversi_cell,
    reversi_game
    
)
     

log = Log("keybd").logger


WHITE_BUTTON = '\u25ef'     # ◯
BLACK_BUTTON = '\u2b24'   # ⬤ 
EMPTY_BUTTON = "."

# NUMS_IN_CIRCLE = {0:9450, 1:9312, 2:9313, 3:9314, 4:9315, 5:9316, 6:9317, 7:9318, 8:9319, 9:9320,
#                   10:9321, 11:9322, 12:9323, 13:9324, 14:9325, 15:9326, 16:9327, 17:9328, 18:9329, 19:9330
#                   }



def build_initial_game_markup(header_buttons=None, footer_buttons=None):
    """
    header_ and footer_buttons: List[List[InlineKeyboardButton]]
    so may be multiline
    """
    
    menu = []
    if not header_buttons:
        header_buttons = get_default_header_buttons()
    menu.extend(header_buttons)
    
    game_board = get_initial_gameboard()
    menu.extend(game_board)
    
    if not footer_buttons:
        footer_buttons = get_default_footer_buttons()
    menu.extend(footer_buttons)

    log.info("initial game menu constructed")
    return InlineKeyboardMarkup(menu)

def build_game_markup(header_buttons=None, footer_buttons=None):
    """
    header_ and footer_buttons: List[List[InlineKeyboardButton]]
    so may be multiline
    """
    
    menu = []
    if not header_buttons:
        header_buttons = get_default_header_buttons()
    menu.extend(header_buttons)
    
    game_board = get_gameboard()
    menu.extend(game_board)
    
    if not footer_buttons:
        footer_buttons = get_default_footer_buttons()
    menu.extend(footer_buttons)

    # log.info("game board constructed")
    return InlineKeyboardMarkup(menu)

    

def get_default_header_buttons():
    return []

def get_default_footer_buttons():
    footer_buttons = [
        [InlineKeyboardButton("stop game", callback_data="stop_game"), InlineKeyboardButton(" - ", callback_data="1.2")],
        [InlineKeyboardButton("- ", callback_data="2.0")]
    ]
    return footer_buttons


def get_initial_gameboard():
    board_state = reversi_game.get_initial_board_state()
    board = generate_gameboard(board_state)
    return board

def get_gameboard():
    board_state = reversi_game.get_board_state()
    board = generate_gameboard(board_state)
    return board

def generate_gameboard(board_state):
    board_size = len(board_state)
    board = []
    for y in range(board_size):
        row = []
        for x in range(board_size):
            if board_state[y][x] == reversi_cell.EMPTY:
                cell_text = EMPTY_BUTTON
                cell_data = f"e:{y}:{x}"
            elif board_state[y][x] == reversi_cell.BLACK:        
                cell_text = BLACK_BUTTON
                cell_data = f"b:{y}:{x}"
            elif board_state[y][x] == reversi_cell.WHITE:        
                cell_text = WHITE_BUTTON
                cell_data = f"w:{y}:{x}"
            else:     
                cell_text = "*"
                cell_data = f"e:{y}:{x}"
            
            cell_button = InlineKeyboardButton(text=cell_text, callback_data=cell_data)
            row.append(cell_button)
        board.append(row)
    return board
    




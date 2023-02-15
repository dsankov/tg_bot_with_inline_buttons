from aiogram import types
from button_bot.callback_datas import cell_CallbackData
from button_bot.callback_datas import game_board, BOARD_SIZE



WHITE_CIRCLE = '\u25ef'     # ◯
BLACK_CIRCLE = '\u2b24'     # ⬤ 
NUMS_IN_CIRCLE = {0:9450, 1:9312, 2:9313, 3:9314, 4:9315, 5:9316, 6:9317, 7:9318, 8:9319, 9:9320,
                  10:9321, 11:9322, 12:9323, 13:9324, 14:9325, 15:9326, 16:9327, 17:9328, 18:9329, 19:9330
                  }



def get_game_board():
    board_markup = types.InlineKeyboardMarkup(row_width=BOARD_SIZE)
    for y in range(BOARD_SIZE):
        row_markup = []
        for x in range(BOARD_SIZE):
            if game_board[y][x] == 1:
                cell_text = WHITE_CIRCLE 
            elif game_board[y][x] == -1:
                cell_text = BLACK_CIRCLE 
            elif game_board[y][x] == 0:
                cell_text = '\u2003' # space
            else:
                cell_text = chr(NUMS_IN_CIRCLE[game_board[y][x]])

            cell_coord = 'cell:' + str(y) + ':' + str(x)
            row_markup.append(
                types.InlineKeyboardButton(
                    cell_text, 
                    callback_data=cell_CallbackData.new(y=y, x=x)
                    )
                )

        board_markup.row(*row_markup)

    return board_markup
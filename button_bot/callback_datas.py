from aiogram.utils.callback_data import CallbackData

cell_CallbackData = CallbackData("cell", "y", "x")

BOARD_SIZE = 8
game_board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
game_board[3][3], game_board[4][4] = 1, 1
game_board[3][4], game_board[4][3] = -1, -1
game_board[0][0] = 2
game_board[0][1] = 3
game_board[0][2] = 18
from enum import Enum

BOARD_SIZE = 8
class reversi_cells(Enum):
    CELL_EMPTY = 0
    CELL_BLACK = -1
    CELL_WHITE = -2


def get_initial_board_state():
    """
    returns -> List[List[reversi_cells]]:
    """
    
    board = [[reversi_cells.CELL_EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[3][4], board[4][3] = reversi_cells.CELL_BLACK, reversi_cells.CELL_BLACK
    board[3][3], board[4][4] = reversi_cells.CELL_WHITE, reversi_cells.CELL_WHITE

    return board

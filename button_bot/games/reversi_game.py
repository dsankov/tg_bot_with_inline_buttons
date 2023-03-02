from enum import Enum
from typing import List
BOARD_SIZE = 8
class reversi_cell(Enum):
    EMPTY = 0
    BLACK = -1
    WHITE = -2
    
class reversi_player(Enum):
    BLACK = 1
    WHITE = 2

class reversiGame:
    def __init__(self) -> None:
        self.board = [[reversi_cell.EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        
    def get_initial_board_state(self):
        """
        returns -> List[List[reversi_cell]]:
        """    
        self.board[3][4], self.board[4][3] = reversi_cell.BLACK, reversi_cell.BLACK
        self.board[3][3], self.board[4][4] = reversi_cell.WHITE, reversi_cell.WHITE

        return self.board
    
    def get_board_state(self):
        return self.board
    
    def make_move(self, player: int, position: List):
        y, x = position[0], position[1]
        assert self.board[y][x] == reversi_cell.EMPTY
        if player == reversi_player.BLACK:
            self.board[y][x] = reversi_cell.BLACK
        else:
            self.board[y][x] = reversi_cell.WHITE
    
    def availiable_moves(self):
        return []
                
reversi_game = reversiGame()
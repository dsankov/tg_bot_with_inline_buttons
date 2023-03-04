from enum import Enum
from typing import List
from log2d import Log
import copy

BOARD_SIZE = 8
class reversi_cell(Enum):
    EMPTY = 0
    BLACK = -1
    WHITE = -2
    
class reversi_player(Enum):
    BLACK = -1
    WHITE = -2
    
log = Log("game").logger

class Board:
    # _board: list[list[reversi_cell]]
    def __init__(self, board: list[list[reversi_cell]] = None) -> None:
        if not board:
            self._board = [[reversi_cell.EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
            self._board[3][4], self._board[4][3] = reversi_cell.BLACK, reversi_cell.BLACK
            self._board[3][3], self._board[4][4] = reversi_cell.WHITE, reversi_cell.WHITE
        else:
            self._board = copy.deepcopy(board)
    def get_board_state(self) -> list[list[reversi_cell]]:
        return self._board
    def cell_on_board(self, position: tuple[int, int]) -> bool:
        return (
            0 <= position[0] < BOARD_SIZE and
            0 <= position[1] < BOARD_SIZE
        )
    
    def get_cell(self, position: tuple[int, int]) -> reversi_cell | None:
        if self.cell_on_board(position):
            return self._board[position[0]][position[1]]
        return None
    
    def set_cell(self, position: tuple[int, int], player: reversi_player) -> None:
        y, x = position[0], position[1]
        if player == reversi_player.BLACK:
            self._board[y][x] = reversi_cell.BLACK
        else:
            self._board[y][x] = reversi_cell.WHITE
    
    def next_to(self, position, direction, step) -> tuple[int, int] | None:
        target_position = (position[0] + step * direction[0], position[1] + step * direction[1])
        return target_position
        # if self.cell_on_board(target_position):
        #     return target_position
        # return None
    
    def mark_direction(self, position: tuple[int, int], direction: tuple[int, int], player: reversi_player) -> int: # directiom_score
        if player == reversi_player.BLACK:
            # player = reversi_cell.BLACK
            opposite_player = reversi_player.WHITE
            opposite_player_cell = reversi_cell.WHITE
        else:
            opposite_player = reversi_player.BLACK
            opposite_player_cell = reversi_cell.BLACK
        
        step = 1
        next_cell = self.next_to(position, direction, step)
        if self.cell_on_board(next_cell):
            if self.get_cell(next_cell) != opposite_player_cell:
                # log.info(self.get_cell(next_cell))
                return 0
            
            direction_score = 1
            step += 1
            next_cell = self.next_to(position, direction, step)
            while self.cell_on_board(next_cell):
                if self.get_cell(next_cell) == reversi_cell.EMPTY:
                    return 0
                elif self.get_cell(next_cell) == opposite_player_cell:
                    direction_score += 1
                    step += 1
                    next_cell = self.next_to(position, direction, step)
                else:
                    for i in range(direction_score + 1):
                        cell_to_mark = self.next_to(position, direction, i)
                        self.set_cell(cell_to_mark, player)
                    return direction_score
                
            # no current player's cells in this direction found before board edge
        return 0
    
    def make_move(self, position: tuple[int, int], player: reversi_player) -> int: # move_score
        directions = (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0 , 1),
            (1, -1),  (1, 0),  (1,  1)
        )
        move_score = 0
        for direction in directions:
            direction_score = self.mark_direction(position, direction, player)
            move_score += direction_score
        if move_score > 0:
            self.set_cell(position, player)
        return move_score
    
    def availiable_moves(self):
        return []

class reversiGame:
    def __init__(self) -> None:
        pass
            
    def get_initial_board_state(self):
        """
        returns -> List[List[reversi_cell]]:
        """    
        self._board = Board()
        return self._board.get_board_state()
    
    def get_board_state(self) -> list[list[reversi_cell]]:
        return self._board.get_board_state()
    
    def make_move(self, player: reversi_player, position: tuple[int, int]):
        y, x = position[0], position[1]
        assert self._board.get_cell(position) == reversi_cell.EMPTY
        # self.evaluate_move(player, position)
        move_score, result_board = self.emulate_move(position, player)
        if move_score > 0:
            self._board = result_board
            
    
    def emulate_move(self, position: tuple[int, int], player: reversi_player,) -> tuple[int, Board]:
        
        resulted_board = Board(self._board.get_board_state())
        # resulted_board.set_cell(position, player)
        move_score = resulted_board.make_move(position, player)
        # if move_score > 0:
        #     self._board = resulted_board
        
        # move_score = 0
        # board = copy.deepcopy(self.board)
        # for direction in directions:
        #     direction_score = self.evaluate_direction(player, position, direction)
        #     move_score += direction_score
        #     # if self.cell_on_board(position=self.next_to(position, direction)):
        #     log.info(f"cell:{position} direction:{direction} score:{direction_score}")
        # log.info(f"cell:{position} score:{move_score}")   
        return (move_score, resulted_board)
        
    

                
    def get_score(self) -> dict[reversi_player]:
        black_score, white_score = 0, 0
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self._board.get_cell((y,x)) == reversi_cell.BLACK:
                    black_score += 1
                elif self._board.get_cell((y,x)) == reversi_cell.WHITE:
                    white_score += 1
                else:
                    pass
        return {
            reversi_player.BLACK: black_score,
            reversi_player.WHITE: white_score
        }
     
    # def evaluate_direction(self, player: reversi_player, position, direction):

                               
        
    
reversi_game = reversiGame()
#  (C) Copyright Wieger Wesselink 2021. Distributed under the GPL-3.0-or-later
#  Software License, (See accompanying file LICENSE or copy at
#  https://www.gnu.org/licenses/gpl-3.0.txt)

import random
import time
import copy
import re
import math
from competitive_sudoku.sudoku import GameState, Move, SudokuBoard, TabooMove
import competitive_sudoku.sudokuai


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def __init__(self):
        super().__init__()

        """
        Player_squares() seem to give an incorrect output which leads to "illegal move"
        """

    def compute_best_move(self, game_state: GameState) -> None:
        depth = 1
        _, best_move = self.minimax(game_state, depth, True)
        
        print(f'value is , {best_move}')
             
        self.propose_move(Move(best_move.square, best_move.value))  # needs to be able to return a move every second
        # if game_state.current_player() == 1:
        #     value = self.minimax(game_state, depth, True)
        #     prin
        # else:
        #     value = self.minimax(game_state, depth, False)







    def get_valid_moves(self, game_state: GameState):
        N = game_state.board.N

        # Check whether a cell is empty, a value in that cell is not taboo, and that cell is allowed
        def possible(i, j, value):
                return (
                game_state.board.get((i, j)) == SudokuBoard.empty
                and not TabooMove((i, j), value) in game_state.taboo_moves
                and (i, j) in game_state.player_squares()
                and value not in [game_state.board.get((i, col)) for col in range(game_state.board.N) if col != j]
                and value not in [game_state.board.get((row, j)) for row in range(game_state.board.N) if row != i]
                and value not in [game_state.board.get((r,c)) 
                    for r in range(i // game_state.board.region_height() * game_state.board.region_height(),
                        (i // game_state.board.region_height() + 1) * game_state.board.region_height())
                    for c in range(j // game_state.board.region_width() * game_state.board.region_width(),
                        (j // game_state.board.region_width() + 1) * game_state.board.region_width())]
                )

        return [
            Move((i, j), value)
            for i in range(N)
            for j in range(N)
            for value in range(1, N + 1)
            if possible(i, j, value)
        ]

    def evaluate(self, game_state: GameState):
            print(f'evaluation {game_state.scores[0] - game_state.scores[1]}')
            return game_state.scores[0] - game_state.scores[1]
    
    def getChildren(self, game_state: GameState):
            return self.get_valid_moves(game_state)

    def minimax(self, game_state: GameState, depth, isMaximizingPlayer):
        if depth == 0: # or state.isfinishe
            return (self.evaluate(game_state), Move(0,0))

        children = self.getChildren(game_state)

        if isMaximizingPlayer:
            best_value = -math.inf
            best_move = None
            for child in children:
                print(f'output minimax {self.minimax(game_state, depth-1, False)}')
                value, _ = self.minimax(game_state, depth-1, False)
                if value > best_value:
                     best_value = value
                     best_move = child  
                #value = max(value, self.minimax(child, depth-1, False))
            return value, best_move

        else:
            best_value = math.inf
            best_move = None
            for child in children:
                value, _ = self.minimax(game_state, depth-1, True)
                if value < best_value:
                     best_value = value
                     best_move = child
                # value = max(value, self.minimax(game_state, depth-1, True))
            return value, best_move


    # def is_solvable(self, game_state: GameState, square, value, N):

    #     board = copy.deepcopy(game_state.board)
    #     #print(board)
    #     def is_valid_move(board, row, col, num):
    #         """Checks if placing num in (row, col) is valid."""
    #         for i in range(N):
    #             if board.get((row, i)) == num or board.get((i, col)) == num:
    #                 # print(f'{board.get((row, i))},  {board.get((i, col))}, {num}')
    #                 return False

    #         # Check subgrid

    #         box_start_row = (row // game_state.board.region_height()) * game_state.board.region_height()
    #         box_start_col = (col // game_state.board.region_width()) * game_state.board.region_width()
    #         for r in range(box_start_row, box_start_row + game_state.board.region_height()):
    #             for c in range(box_start_col, box_start_col + game_state.board.region_width()):
    #                 if board.get((r, c)) == num:
    #                     return False
    #         return True

    #     def solve(board):
    #         for row in range(N):
    #             for col in range(N):
    #                 if board.get((row, col)) == SudokuBoard.empty:
    #                     for num in range(1, N+1):
    #                         if is_valid_move(board, row, col, num):
    #                             board.put((row, col), num)
    #                             if solve(board):
    #                                 return True
    #                             board.put((row, col), SudokuBoard.empty)
    #                     return False
    #         return True

    #     row, col = square
    #     if not is_valid_move(board, row, col, value):   # THIS FIXED THE FUNCTION
    #         return False

    #     board.put(square, value)
    #     solvable = solve(board)
    #     #print(solva  ble)
    #     return solvable

    # def compute_best_move(self, game_state: GameState) -> None:
    #     N = game_state.board.N

    #     all_possible_moves = []
    #     #print(game_state.player_squares())
    #     for square in game_state.player_squares():
    #         for value in range(1, N + 1):
    #             #print(f'solving for {square} -> {value}')
    #             if game_state.board.get(square) == SudokuBoard.empty and not TabooMove(square, value) in game_state.taboo_moves:
    #                 if self.is_solvable(game_state, square, value, N):
    #                     #print(f'solvable {square} -> {value}')
    #                     all_possible_moves.append((square, value))

    #     print(all_possible_moves)
    #     square, value = random.choice(all_possible_moves)
    #     print(f"proposed move is = {square, value}")
    #     self.propose_move(Move(square, value))

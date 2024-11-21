#  (C) Copyright Wieger Wesselink 2021. Distributed under the GPL-3.0-or-later
#  Software License, (See accompanying file LICENSE or copy at
#  https://www.gnu.org/licenses/gpl-3.0.txt)
import copy
import random
import time
from competitive_sudoku.sudoku import GameState, Move, SudokuBoard, TabooMove
import competitive_sudoku.sudokuai


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def __init__(self):
        super().__init__()

    # N.B. This is a very naive implementation.
    def compute_best_move(self, game_state: GameState) -> None:
        N = game_state.board.N
        taboo_moves = ' '.join(f'{move.square[0]} {move.square[1]} {move.value}' for move in game_state.taboo_moves)
        board = game_state.board
        board_text = str(board)
        player_squares = game_state.player_squares()
        print (f"board text= {game_state.board} and taboo moves = {taboo_moves} and playerSquares = {player_squares}")

        def get_valid_moves(self,game_state):
            N = game_state.board.N
            # Check whether a cell is empty, a value in that cell is not taboo, and that cell is allowed
            def possible(i, j, value):
                return (game_state.board.get((i, j)) == SudokuBoard.empty
                       and not TabooMove((i, j), value) in game_state.taboo_moves
                           and (i, j) in game_state.player_squares()
                            and value not in [game_state.board.get((i, col))
                                              for col in range(game_state.board.N) if col != j]  #check other cells in the same row
                            and value not in [game_state.board.get((row, j))
                                              for row in range(game_state.board.N) if row != i]  #check other cells in the same column
                and not any(
                    game_state.board.get((r, c)) == value
                    for r in range((i // game_state.board.region_height()) * game_state.board.region_height(),
                                   ((i // game_state.board.region_height()) + 1) * game_state.board.region_height())
                    for c in range((j // game_state.board.region_width()) * game_state.board.region_width(),
                                   ((j // game_state.board.region_width()) + 1) * game_state.board.region_width())
                    )
                )
            return [Move((i, j), value) for i in range(N) for j in range(N)
                         for value in range(1, N+1) if possible(i, j, value)]


        move=random.choice(get_valid_moves(self,game_state))
        self.propose_move(move)
        """while True:
            time.sleep(0.2)
            self.propose_move(get_valid_moves(self,game_state))"""



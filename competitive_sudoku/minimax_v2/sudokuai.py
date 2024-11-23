import random
import copy
from competitive_sudoku.sudoku import GameState, Move, TabooMove, SudokuBoard
import competitive_sudoku.sudokuai
from typing import Tuple

class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration using Minimax.
    """

    def __init__(self):
        super().__init__()

    # def get_valid_moves(self, game_state):
    #     N = game_state.board.N

    #     # print(f"{game_state.player_squares()=}")
    #     def possible(i, j, value):
    #         return (
    #             game_state.board.get((i, j)) == SudokuBoard.empty
    #             and not TabooMove((i, j), value) in game_state.taboo_moves
    #             and (i, j) in game_state.player_squares()
    #             and value
    #             not in [
    #                 game_state.board.get((i, col))
    #                 for col in range(game_state.board.N)
    #                 if col != j
    #             ]
    #             and value
    #             not in [
    #                 game_state.board.get((row, j))
    #                 for row in range(game_state.board.N)
    #                 if row != i
    #             ]
    #             and not any(
    #                 game_state.board.get((r, c)) == value
    #                 for r in range(
    #                     (i // game_state.board.region_height())
    #                     * game_state.board.region_height(),
    #                     ((i // game_state.board.region_height()) + 1)
    #                     * game_state.board.region_height(),
    #                 )
    #                 for c in range(
    #                     (j // game_state.board.region_width())
    #                     * game_state.board.region_width(),
    #                     ((j // game_state.board.region_width()) + 1)
    #                     * game_state.board.region_width(),
    #                 )
    #             )
    #         )

    #     return [
    #         Move((i, j), value)
    #         for i in range(N)
    #         for j in range(N)
    #         for value in range(1, N + 1)
    #         if possible(i, j, value)
    #     ]

    def simulate_move(self, game_state: GameState, move: Move):
        """
        Simulates a move and returns a new game state.
        """
        new_state = copy.deepcopy(game_state)
        new_state.board.put(move.square, move.value)
        return new_state

    def get_valid_moves(self, game_state: GameState):
        """
        ours was failing and this one works
        """
        N = game_state.board.N

        def is_valid_move(square, value):
            return (
                game_state.board.get(square) == SudokuBoard.empty
                and not TabooMove(square, value) in game_state.taboo_moves
                and (square in game_state.player_squares() if game_state.player_squares() is not None else True)
                and value not in [game_state.board.get((square[0], col)) for col in range(N)]
                and value not in [game_state.board.get((row, square[1])) for row in range(N)]
                and value not in self.get_region_values(game_state.board, square)
            )

        valid_moves = [
            Move((i, j), value)
            for i in range(N)
            for j in range(N)
            for value in range(1, N + 1)
            if is_valid_move((i, j), value)
        ]
        return valid_moves

    def get_region_values(self, board: SudokuBoard, square: Tuple[int, int]):
        """
        Gets the values in the region corresponding to the given square.
        """
        region_width = board.region_width()
        region_height = board.region_height()
        start_row = (square[0] // region_height) * region_height
        start_col = (square[1] // region_width) * region_width

        region_values = [
            board.get((r, c))
            for r in range(start_row, start_row + region_height)
            for c in range(start_col, start_col + region_width)
        ]
        return region_values

    def is_terminal(self, game_state: GameState):
        """
        Checks if the game state is terminal (no valid moves left).
        """
        return len(self.get_valid_moves(game_state)) == 0

    def evaluate(self, game_state: GameState):
        """
        Evaluates the game state with a heuristic based on the score and potential moves.
        """
        return sum(game_state.scores)

    def minimax(self, game_state: GameState, depth: int, maximizing: bool):
        """
        Minimax implementation with depth-limited search.
        """
        if depth == 0 or self.is_terminal(game_state):
            return self.evaluate(game_state)

        valid_moves = self.get_valid_moves(game_state)

        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                next_state = self.simulate_move(game_state, move)
                eval = self.minimax(next_state, depth - 1, maximizing=False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                next_state = self.simulate_move(game_state, move)
                eval = self.minimax(next_state, depth - 1, maximizing=True)
                min_eval = min(min_eval, eval)
            return min_eval

    def compute_best_move(self, game_state: GameState) -> None:
        """
        Minimax with only depth 2 :()
        """
        depth = 2 # Anything more it loses cuz it too slow :(
        valid_moves = self.get_valid_moves(game_state)

        best_move = None
        best_score = float('-inf')

        for move in valid_moves:
            next_state = self.simulate_move(game_state, move)
            score = self.minimax(next_state, depth, maximizing=False)
            if score > best_score:
                best_score = score
                best_move = move

        self.propose_move(best_move)
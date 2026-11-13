
import unittest
from game import PegSolitaire


class TestPegSolitaire(unittest.TestCase):

    # User Story 1: Choose a board size
    # AC 1.3
    def test_choose_board_size(self):
        game = PegSolitaire(board_size=7, board_type="English")

        game.board_size = 9

        self.assertEqual(game.board_size, 9)


    # User Story 2: Choose the board type
    # AC 2.2
    def test_choose_board_type(self):
        game = PegSolitaire(board_size=7, board_type="English")

        game.board_type = "Diamond"

        self.assertEqual(game.board_type, "Diamond")


    # User Story 3: Start a new game
    # AC 3.2
    def test_new_game_initialization(self):
        game = PegSolitaire(board_size=7, board_type="English")

        game.new_game()

        # Center position should be empty
        self.assertEqual(game.board[3][3], 0)

        # All other playable positions should contain pegs
        for row in range(7):
            for col in range(7):
                if game.board[row][col] is not None:
                    if (row, col) != (3, 3):
                        self.assertEqual(game.board[row][col], 1)


    # User Story 4: Make a move
    # AC 4.1 and 4.3
    def test_valid_move(self):
        game = PegSolitaire(board_size=7, board_type="English")
        game.new_game()

        # Move peg from (3, 1) over (3, 2) into (3, 3)
        result = game.make_move((3, 1), (3, 3))

        self.assertTrue(result)

        # Starting position is now empty
        self.assertEqual(game.board[3][1], 0)

        # Jumped peg has been removed
        self.assertEqual(game.board[3][2], 0)

        # Destination now contains the moved peg
        self.assertEqual(game.board[3][3], 1)


    # User Story 5: A game is over
    # AC 5.1 and 5.2
    def test_game_over_with_one_peg(self):
        game = PegSolitaire(board_size=7, board_type="English")
        game.new_game()

        # Remove all pegs except the center
        for row in range(7):
            for col in range(7):
                if game.board[row][col] is not None:
                    game.board[row][col] = 0

        game.board[3][3] = 1

        # Game should be over
        self.assertTrue(game.is_game_over())

        # Exactly one peg should remain
        peg_count = sum(
            cell == 1
            for row in game.board
            for cell in row
        )

        self.assertEqual(peg_count, 1)

    
    def test_automated_move(self):
        game = PegSolitaire()

        initial_pegs = sum(
            row.count(1) for row in game.board
        )

        result = game.make_automated_move()

        remaining_pegs = sum(
            row.count(1) for row in game.board
        )

        self.assertTrue(result)
        self.assertEqual(
            remaining_pegs,
            initial_pegs - 1
        )


    def test_randomize_board(self):
        game = PegSolitaire()

        # Count pegs before randomization
        original_pegs = sum(
            row.count(1) for row in game.board
        )

        # Record valid board positions
        original_valid_cells = [
            (r, c)
            for r in range(game.board_size)
            for c in range(game.board_size)
            if game.board[r][c] is not None
        ]

        # Randomize the board
        game.randomize_board()

        # Count pegs after randomization
        randomized_pegs = sum(
            row.count(1) for row in game.board
        )

        randomized_valid_cells = [
            (r, c)
            for r in range(game.board_size)
            for c in range(game.board_size)
            if game.board[r][c] is not None
        ]

        # Verify peg count is unchanged
        self.assertEqual(original_pegs, randomized_pegs)

        # Verify board shape is unchanged
        self.assertEqual(
            original_valid_cells,
            randomized_valid_cells
        )

    def test_game_rating(self):
        game = PegSolitaire()

        # An active game should have no rating
        self.assertIsNone(game.get_game_rating())

        # Create a completed game with one peg
        for row in range(game.board_size):
            for col in range(game.board_size):
                if game.board[row][col] is not None:
                    game.board[row][col] = 0

        game.board[3][3] = 1

        self.assertEqual(
            game.get_game_rating(),
            "Outstanding"
        )

if __name__ == "__main__":
    unittest.main()

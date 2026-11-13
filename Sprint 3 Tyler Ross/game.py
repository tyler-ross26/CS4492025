import random
import json
from pathlib import Path

class PegSolitaire:

    def __init__(self, board_size=7, board_type="English"):
        self.board_size = board_size
        self.board_type = board_type

        self.recording = False
        self.recorded_events = []
        self.initial_board = None

        self.new_game()

    def initialize_board(self):
        center = self.board_size // 2
        # Initialize the board based on the selected size and type, allowing sizes ranging from 5 to 15 and types "English", "Diamond", or "Hexagonal"
        if self.board_size not in [5, 7, 9, 11, 13, 15]:
            raise ValueError("Board size must be an odd number between 5 and 15.")
        elif self.board_type not in ["English", "Diamond", "Hexagonal"]:
            raise ValueError("Board type must be 'English', 'Diamond', or 'Hexagonal'.")
        elif self.board_type == "English":
            # Create a 2D list representing the English board
            # Scale the width of the cross with the board size
            arm_width = max(1, self.board_size // 3)
            half_width = arm_width // 2
            return [
                [
                    1 if (
                        abs(i - center) <= half_width or
                        abs(j - center) <= half_width
                    ) else None
                    for j in range(self.board_size)
                ]
                for i in range(self.board_size)
            ]
        elif self.board_type == "Diamond":
            # Create a 2D list representing the Diamond board
            board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
            center = self.board_size // 2
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if abs(row - center) + abs(col - center) <= center:
                        board[row][col] = 1  # Peg present
                    else:
                        board[row][col] = None  # Invalid position
            return board
        elif self.board_type == "Hexagonal":
            return [
                [
                    1 if (
                        abs(i - center) <= center and
                        abs(j - center) <= center and
                        abs((i - center) + (j - center)) <= center
                    ) else None
                    for j in range(self.board_size)
                ]
                for i in range(self.board_size)
            ]

    def change_board(self, board_size, board_type):
        if board_size not in [5, 7, 9, 11, 13, 15]:
            raise ValueError("Board size must be an odd number between 5 and 15.")
        if board_type not in ["English", "Diamond", "Hexagonal"]:
            raise ValueError("Board type must be 'English', 'Diamond', or 'Hexagonal'.")
        self.board_size = board_size
        self.board_type = board_type
        self.new_game()

    def new_game(self):
        # Reset the board to the initial state
        self.board = self.initialize_board()
        # Set the center position to empty
        center = self.board_size // 2
        self.board[center][center] = 0

    def is_valid_move(self, start_pos, end_pos):
        # Validate if a move from start_pos to end_pos is valid
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Check board boundaries
        if not (0 <= start_row < self.board_size and
            0 <= start_col < self.board_size and
            0 <= end_row < self.board_size and
            0 <= end_col < self.board_size):
            return False

        row_diff = start_row - end_row
        col_diff = start_col - end_col

        if (row_diff, col_diff) not in self.get_directions():
            return False

        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2

        return (
            self.board[start_row][start_col] == 1 and
            self.board[mid_row][mid_col] == 1 and
            self.board[end_row][end_col] == 0
        )

    
    def randomize_board(self):
        # Get all valid positions on the board
        valid_positions = []

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] is not None:
                    valid_positions.append((row, col))

        # Count how many pegs are currently on the board
        peg_count = sum(
            row.count(1) for row in self.board
        )

        # Shuffle the valid positions
        random.shuffle(valid_positions)

        # Empty every valid position
        for row, col in valid_positions:
            self.board[row][col] = 0

        # Redistribute the pegs
        for row, col in valid_positions[:peg_count]:
            self.board[row][col] = 1

        # Record the resulting board state
        if self.recording:
            self.recorded_events.append({
                "type": "randomize",
                "board": [
                    row.copy() for row in self.board
                ]
            })

    def make_move(self, start_pos, end_pos):
        if self.is_game_over():
            return False  # No moves can be made if the game is over

        if not self.is_valid_move(start_pos, end_pos):
            return False  # Move is invalid

        start_row, start_col = start_pos
        end_row, end_col = end_pos

        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2

        
        self.board[start_row][start_col] = 0
        self.board[mid_row][mid_col] = 0
        self.board[end_row][end_col] = 1

        # Record the move if recording is enabled
        if self.recording:
            self.recorded_events.append({
                "type": "move",
                "start": list(start_pos),
                "end": list(end_pos)
            })

        return True

    def get_directions(self):
        # Return the possible jump directions based on the board type
        if self.board_type == "Hexagonal":
            return [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, 2), (2, -2)]
        else:
            return [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]

    def get_valid_moves(self):
        valid_moves = []

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 1:

                    for dr, dc in self.get_directions():
                        end_row = row + dr
                        end_col = col + dc

                        start = (row, col)
                        end = (end_row, end_col)

                        if self.is_valid_move(start, end):
                            valid_moves.append((start, end))

        return valid_moves

    
    
    def make_automated_move(self):
        valid_moves = self.get_valid_moves()

        if not valid_moves:
            return False

        start, end = random.choice(valid_moves)

        return self.make_move(start, end)


    def has_valid_moves(self):
        directions = self.get_directions()

        # Check if there are any valid moves left
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 1:
                    # Check all possible jump directions
                    for dr, dc in directions:
                        end_row = row + dr
                        end_col = col + dc
                        if self.is_valid_move((row, col), (end_row, end_col)):
                            return True

        return False

    def is_game_over(self):
        remaining_pegs = sum(
            row.count(1) for row in self.board
        )

        if remaining_pegs <= 1:
            return True

        return not self.has_valid_moves()

    def get_game_result(self):
        if self.is_game_over():
            remaining_pegs = sum(row.count(1) for row in self.board)
            if remaining_pegs == 1:
                return "Win"
            else:
                return "Lose"
        else:
            return "Game is still in progress"

    def get_game_rating(self):
        if not self.is_game_over():
            return None

        remaining_pegs = sum(
            row.count(1) for row in self.board
        )

        if remaining_pegs == 1:
            return "Outstanding"
        elif remaining_pegs == 2:
            return "Very Good"
        elif remaining_pegs == 3:
            return "Good"
        else:
            return "Average"

    def start_recording(self):
        # Begin recording the current game
        self.recording = True
        self.recorded_events = []

        # Save a copy of the current board
        self.initial_board = [
            row.copy() for row in self.board
        ]

    def stop_recording(self):
        # Stop recording new events
        self.recording = False

    def save_recording(self, filename="game_recording.json"):
        if self.initial_board is None:
            return False

        recording_data = {
            "board_size": self.board_size,
            "board_type": self.board_type,
            "initial_board": self.initial_board,
            "events": self.recorded_events
        }

        # Save relative filenames in the project folder
        file_path = Path(filename)

        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parent / file_path

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(recording_data, file, indent=4)

        return True

    def load_recording(self, filename="game_recording.json"):
        file_path = Path(filename)

        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parent / file_path

        # Read the recorded game
        with open(file_path, "r", encoding="utf-8") as file:
            recording_data = json.load(file)

        # Stop any active recording
        self.recording = False

        # Restore the board settings
        self.board_size = recording_data["board_size"]
        self.board_type = recording_data["board_type"]

        # Restore the starting board
        self.board = [
            row.copy()
            for row in recording_data["initial_board"]
        ]

        # Load recorded events
        self.recorded_events = recording_data["events"]

        # Reset replay position
        self.replay_index = 0

        return True

    def replay_next_event(self):
        # Stop if every event has been replayed
        if self.replay_index >= len(self.recorded_events):
            return False

        event = self.recorded_events[self.replay_index]

        if event["type"] == "move":
            start = tuple(event["start"])
            end = tuple(event["end"])

            # Execute the recorded move
            if not self.make_move(start, end):
                raise ValueError(
                    f"Invalid recorded move at event {self.replay_index}"
                )

        elif event["type"] == "randomize":
            # Restore the exact randomized board
            self.board = [
                row.copy() for row in event["board"]
            ]

        else:
            raise ValueError(
                f"Unknown event type: {event['type']}"
            )

        self.replay_index += 1
        return True

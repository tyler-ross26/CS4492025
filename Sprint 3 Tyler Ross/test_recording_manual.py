
from game import PegSolitaire

game = PegSolitaire()

game.start_recording()

# Make one valid move
game.make_move((3, 1), (3, 3))

# Randomize the board
game.randomize_board()

game.stop_recording()

# Save to file
success = game.save_recording()

print("Recording saved:", success)
print("Events recorded:", len(game.recorded_events))
print("Recorded events:", game.recorded_events)
import os
print("File saved at:", os.path.abspath("game_recording.json"))

from game import PegSolitaire

# Create a game and load the recording
game = PegSolitaire()

game.load_recording("game_recording.json")

print("Board type:", game.board_type)
print("Board size:", game.board_size)
print("Events loaded:", len(game.recorded_events))

# Replay every event
while game.replay_next_event():
    print("Replayed event:", game.replay_index)

print("Replay complete!")
print("Final board:")

for row in game.board:
    print(row)


import tkinter as tk
from game import PegSolitaire


class PegSolitaireGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.geometry("950x650")

        # Create the game
        self.game = PegSolitaire()
        self.selected_peg = None
        self.autoplay_running = False
        self.replay_running = False
        self.autoplay_job = None

        # Title
        title = tk.Label(root, text="Peg Solitaire", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Main layout
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        # Left, center, and right sections
        self.left_frame = tk.Frame(main_frame, width=180)
        self.board_frame = tk.Frame(main_frame)
        self.right_frame = tk.Frame(main_frame, width=180)

        self.left_frame.pack(side="left", fill="y", padx=20)
        self.board_frame.pack(side="left", expand=True)
        self.right_frame.pack(side="right", fill="y", padx=20)

        # Board type dropdown
        tk.Label(self.left_frame, text="Board Type").pack(pady=5)

        self.board_type = tk.StringVar(value="English")

        tk.OptionMenu(
            self.left_frame,
            self.board_type,
            "English",
            "Diamond",
            "Hexagonal"
        ).pack(pady=5)

        # Board size dropdown
        tk.Label(self.left_frame, text="Board Size").pack(pady=5)

        self.board_size = tk.IntVar(value=7)

        tk.OptionMenu(
            self.left_frame,
            self.board_size,
            5, 7, 9, 11, 13, 15
        ).pack(pady=5)

        # New game button
        tk.Button(
            self.left_frame,
            text="New Game",
            command=self.new_game
        ).pack(pady=20)


        # Autoplay button
        self.autoplay_button = tk.Button(
            self.left_frame,
            text="Autoplay",
            command=self.start_autoplay
        )
        self.autoplay_button.pack(pady=10)

        # Randomize button
        self.randomize_button = tk.Button(
            self.left_frame,
            text="Randomize",
            command=self.randomize_game
        )
        self.randomize_button.pack(pady=10)


        # Record Game checkbox
        self.record_var = tk.BooleanVar(value=False)

        self.record_checkbox = tk.Checkbutton(
            self.left_frame,
            text="Record Game",
            variable=self.record_var,
            command=self.toggle_recording
        )
        self.record_checkbox.pack(pady=5)

        # Replay Game button
        self.replay_button = tk.Button(
            self.left_frame,
            text="Replay Game",
            command=self.start_replay
        )
        self.replay_button.pack(pady=5)


        # Game status
        tk.Label(
            self.right_frame,
            text="Game Status",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.status_label = tk.Label(
            self.right_frame,
            text="Game in progress",
            wraplength=160
        )
        self.status_label.pack(pady=10)

        # Draw the initial board
        self.draw_board()

    def draw_board(self):
        # Clear the old board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Create squares for playable positions
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):

                cell = self.game.board[row][col]

                if cell is None:
                    continue

                # Green = peg, white = empty
                color = "green" if cell == 1 else "white"

                # Highlight selected peg
                if self.selected_peg == (row, col):
                    color = "yellow"

                square = tk.Button(
                    self.board_frame,
                    bg=color,
                    activebackground=color,
                    width=3,
                    height=1,
                    relief="solid",
                    borderwidth=1,
                    command=lambda r=row, c=col: self.click_cell(r, c)
                )

                square.grid(row=row, column=col, padx=1, pady=1)

    def click_cell(self, row, col):
        # Prevent manual moves during autoplay or when the game is over or while while moves are recorded
        if self.autoplay_running or self.replay_running or self.game.is_game_over():
            return

        # First click selects a peg
        if self.selected_peg is None:
            if self.game.board[row][col] == 1:
                self.selected_peg = (row, col)

        else:
            # Clicking the selected peg deselects it
            if self.selected_peg == (row, col):
                self.selected_peg = None

            # Clicking another peg changes selection
            elif self.game.board[row][col] == 1:
                self.selected_peg = (row, col)

            # Clicking an empty space attempts a move
            else:
                self.game.make_move(self.selected_peg, (row, col))
                self.selected_peg = None

        self.draw_board()

    def start_autoplay(self):
        if self.autoplay_running:
            return

        if self.replay_running:
            return

        if self.game.is_game_over():
            self.update_status()
            return

        self.autoplay_running = True
        self.autoplay_button.config(state="disabled")
        self.selected_peg = None

        self.play_next_move()

    def play_next_move(self):
        self.autoplay_job = None

        if not self.autoplay_running:
            return

        if self.game.is_game_over():
            self.autoplay_running = False
            self.autoplay_button.config(state="normal")
            self.update_status()
            return

        self.game.make_automated_move()

        self.draw_board()
        self.update_status()

        if self.game.is_game_over():
            self.autoplay_running = False
            self.autoplay_button.config(state="normal")
        else:
            self.autoplay_job = self.root.after(
                500,
                self.play_next_move
            )

        self.update_status()

    
    def new_game(self):
        # Stop autoplay if it is running
        self.autoplay_running = False

        # Stop any active replay
        self.replay_running = False


        # Save any active recording before starting a new game
        if self.record_var.get():
            self.game.stop_recording()
            self.game.save_recording()
            self.record_var.set(False)
            print("Recording saved before starting a new game.")


        if self.autoplay_job is not None:
            self.root.after_cancel(self.autoplay_job)
            self.autoplay_job = None

        self.autoplay_button.config(state="normal")

        # Apply selected settings and restart
        self.game.change_board(
            self.board_size.get(),
            self.board_type.get()
        )

        self.selected_peg = None

        self.draw_board()
        self.update_status()

    def update_status(self):
        if self.game.is_game_over():
            rating = self.game.get_game_rating()

            if rating == "Outstanding":
                status = f"Game Won!\nRating: {rating}"
            else:
                status = f"Game Over!\nRating: {rating}"
        else:
            status = "Game In Progress"

        self.status_label.config(text=status)


    def randomize_game(self):
        # Don't randomize during autoplay
        if self.autoplay_running:
            return

        # Don't randomize during replay
        if self.replay_running:
            return

        # Don't randomize after the game ends
        if self.game.is_game_over():
            return

        # Randomize the board
        self.game.randomize_board()

        # Clear selected peg
        self.selected_peg = None

        # Refresh the interface
        self.draw_board()
        self.update_status()
    
    def toggle_recording(self):
        if self.replay_running:
            self.record_var.set(False)
            return
        
        if self.record_var.get():
            # Start recording the current game
            self.game.start_recording()
            print("Recording started.")
        else:
            # Stop recording and save the game
            self.game.stop_recording()

            if self.game.save_recording():
                print("Recording saved to game_recording.json")


    
    def start_replay(self):
        # Don't start replay while autoplay is running
        if self.autoplay_running:
            return

        # Don't start another replay while replay is running
        if self.replay_running:
            return

        # Stop recording before replaying
        if self.record_var.get():
            self.record_var.set(False)
            self.game.stop_recording()
            self.game.save_recording()

        # Load the saved game
        try:
            self.game.load_recording()
        except FileNotFoundError:
            print("No recorded game found.")
            return

        # Clear any selected peg
        self.selected_peg = None

        # Start replay mode
        self.replay_running = True

        # Display the initial board
        self.draw_board()
        self.update_status()

        # Begin replaying events
        self.play_next_replay_event()

    def play_next_replay_event(self):
        if not self.replay_running:
            return

        # Replay the next recorded event
        if self.game.replay_next_event():
            self.draw_board()
            self.update_status()

            # Wait 500 milliseconds before the next event
            self.root.after(500, self.play_next_replay_event)
        else:
            # Replay is complete
            self.replay_running = False
            print("Replay complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PegSolitaireGUI(root)
    root.mainloop()

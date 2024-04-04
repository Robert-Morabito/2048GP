import tkinter as tk

class game(tk.Tk):
    """
    This class uses Tkinter to display a game of 2048
    """
    def __init__(self):
        """
        This function handles calling the initialization for the game screen and logic
        """
        # Ensure parent is initialized
        super().__init__()
        self.title("2048 with GP!")
        self.geometry("400x500")

        # Scoreboard
        self.score = 0
        self.score_label = tk.Label(self, text=f"Score: {self.score}")
        self.score_label.pack(pady=(10,0))

        # Game board
        self.board_frame = tk.Frame(self)
        self.board_frame.pack(pady=30)

        # Initialization
        self.init_board()

    def init_board(self):
        self.tiles = {}
        for i in range(4):
            for j in range(4):
                # Defining the tile structure
                tile_frame = tk.Frame(self.board_frame, width=80, height=80, bg='azure4')
                tile_frame.grid(row=i, column=j, padx=5, pady=5)
                tile_frame.grid_propagate(False)

                # Defining the tile label
                tile_label = tk.Label(tile_frame, text="", bg='LemonChiffon4')
                self.tiles[(i,j)] = tile_label

    def bind_keys(self):
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.bind("<Left>", self.move_left)
        self.bind("<Right>", self.move_right)

    def start_game(self):
        self.score = 0
        # Place initial numbers on the board
        # Reset the board for a new game, if necessary
        self.update_ui()

    def move_up(self, event):
        # Game logic for moving tiles up
        self.update_ui()

    def move_down(self, event):
        # Game logic for moving tiles down
        self.update_ui()

    def move_left(self, event):
        # Game logic for moving tiles left
        self.update_ui()

    def move_right(self, event):
        # Game logic for moving tiles right
        self.update_ui()

    def update_ui(self):
        # Loop through all tiles and update their text based on the game state
        # Update the score label
        for position, tile in self.tiles.items():
            row, col = position
            # Assuming self.board is your game state matrix with the tile values
            value = self.board[row][col] if self.board[row][col] != 0 else ""
            tile.config(text=str(value))

        self.score_label.config(text=f"Score: {self.score}")

if __name__ == "__main__":
    game = game()
    game.mainloop()
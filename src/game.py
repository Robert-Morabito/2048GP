import tkinter as tk
import random


class game(tk.Tk):
    """
    This class uses Tkinter to display a game of 2048
    """

    def __init__(self):
        """
        This function handles calling the initialization for the game screen and logic
        """
        self.tile_colors = {
            2: ("#fffae6", "#4d4d4d"),
            4: ("#fff0b3", "#4d4d4d"),
            8: ("#ffe680", "#4d4d4d"),
            16: ("#ffbf80", "#4d4d4d"),
            32: ("#ffa64d", "#4d4d4d"),
            64: ("#ff751a", "#4d4d4d"),
            128: ("#ffd11a", "#4d4d4d"),
            256: ("#ffd11a", "#4d4d4d"),
            512: ("#ffd11a", "#4d4d4d"),
            1024: ("#ffd11a", "#4d4d4d"),
            2048: ("#ffd11a", "#4d4d4d"),
            4096: ("#1a1400", "#fffae6"),
            8192: ("#1a1400", "#fffae6")}

        # Ensure parent is initialized
        super().__init__()
        self.title("2048 with GP!")
        self.geometry("415x535")

        # Scoreboard
        self.score = 0
        self.score_label = tk.Label(self, text=f"Score: {self.score}", font="Arial 20 bold")
        self.score_label.pack(pady=(10, 0))

        # Reset button
        self.reset = tk.Button(self, text="Replay", command=self.restart_game, font="Arial 12 bold")
        self.reset.pack(pady=(6, 0))

        # Dynamic grid (active layer)
        self.base_grid_frame = tk.Frame(width=210, height=210, bg='#1d1d1d')
        self.base_grid_frame.pack(pady=30)
        self.dynamic_tiles = {}
        self.dynamic_labels = {}
        for i in range(4):
            for j in range(4):
                # Tile frames that house the tile labels
                tile_frame = tk.Frame(self.base_grid_frame, width=80, height=80, bg='gray')
                tile_frame.grid(row=i, column=j, padx=5, pady=5)
                tile_frame.grid_propagate(False)
                self.dynamic_tiles[(i, j)] = tile_frame

                # Tile labels
                tile_label = tk.Label(self.base_grid_frame, text="", font="Arial 16 bold", bg='gray')
                tile_label.grid(row=i, column=j, padx=5, pady=5)
                self.dynamic_labels[(i, j)] = tile_label

        # Keybindings for movement
        self.bind("<Left>", self.move_tiles_left)
        self.bind("<Right>", self.move_tiles_right)
        self.bind("<Up>", self.move_tiles_up)
        self.bind("<Down>", self.move_tiles_down)

    def start_game(self):
        # Place initial numbers on the board
        self.add_new_tile()
        self.add_new_tile()

    def restart_game(self):
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.dynamic_tiles = {}
        self.dynamic_labels = {}
        for i in range(4):
            for j in range(4):
                # Tile frames that house the tile labels
                tile_frame = tk.Frame(self.base_grid_frame, width=80, height=80, bg='gray')
                tile_frame.grid(row=i, column=j, padx=5, pady=5)
                tile_frame.grid_propagate(False)
                self.dynamic_tiles[(i, j)] = tile_frame

                # Tile labels
                tile_label = tk.Label(self.base_grid_frame, text="", font="Arial 16 bold", bg='gray')
                tile_label.grid(row=i, column=j, padx=5, pady=5)
                self.dynamic_labels[(i, j)] = tile_label

        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        """
        This function updates the active layer with a new tile
        """
        # Create a subset of empty tile from the grid
        empty_slots = [(i, j) for i, j in self.dynamic_labels if self.dynamic_labels[(i, j)].cget("text") == ""]
        if empty_slots:
            # Select a random tile from the subset and update its label and color
            i, j = random.choice(empty_slots)
            tile_value = 2 if random.random() < 0.75 else 4
            self.dynamic_tiles[(i, j)].config(bg=self.tile_colors[tile_value][0])  # Change frame background
            self.dynamic_labels[(i, j)].config(text=str(tile_value), bg=self.tile_colors[tile_value][0],
                                               fg=self.tile_colors[tile_value][1])

    def move_tiles_left(self, event):
        moved_or_merged = False
        for i in range(4):
            # Extract the current row values.
            current_row = [int(self.dynamic_labels[(i, j)].cget("text") or 0) for j in range(4)]

            # Consolidate non-zero tiles to the left and prepare for merging.
            consolidated = [value for value in current_row if value != 0]
            new_row = []
            skip_next = False

            # Merge tiles.
            for k in range(len(consolidated)):
                if skip_next:
                    skip_next = False
                    continue
                if k < len(consolidated) - 1 and consolidated[k] == consolidated[k + 1]:
                    new_row.append(consolidated[k] * 2)
                    self.score += consolidated[k] * 2
                    moved_or_merged = True
                    skip_next = True  # Skip the next value since it's merged.
                else:
                    new_row.append(consolidated[k])

            # Fill the rest of the row with zeros (empty spaces).
            new_row.extend([0] * (4 - len(new_row)))

            # Update GUI if there's a change.
            for j, value in enumerate(new_row):
                if current_row[j] != value:
                    moved_or_merged = True
                    bg_color, fg_color = self.tile_colors.get(value, ('gray', 'black'))
                    self.dynamic_tiles[(i, j)].config(bg=bg_color)
                    self.dynamic_labels[(i, j)].config(text=f"{value}" if value else "", bg=bg_color, fg=fg_color)

        if moved_or_merged:
            self.add_new_tile()

        self.score_label.config(text=f"Score: {self.score}")

    def move_tiles_right(self, event):
        moved_or_merged = False
        for i in range(4):
            # Extract the current row values and reverse it for rightward processing.
            current_row = [int(self.dynamic_labels[(i, j)].cget("text") or 0) for j in range(4)]

            # Consolidate non-zero tiles to the right.
            consolidated = [value for value in current_row if value != 0]
            new_row = []
            skip_next = False

            # Merge tiles from right to left, appending to the start of new_row.
            for k in range(len(consolidated) - 1, -1, -1):
                if skip_next:
                    skip_next = False
                    continue
                if k > 0 and consolidated[k] == consolidated[k - 1]:
                    new_row.insert(0, consolidated[k] * 2)
                    self.score += consolidated[k] * 2
                    moved_or_merged = True
                    skip_next = True  # Skip the next (technically previous in the list) value since it's merged.
                else:
                    new_row.insert(0, consolidated[k])

            # Fill the rest of the row with zeros (empty spaces) at the start.
            new_row = [0] * (4 - len(new_row)) + new_row

            # Update GUI if there's a change.
            for j, value in enumerate(new_row):
                if current_row[j] != value:
                    moved_or_merged = True
                    bg_color, fg_color = self.tile_colors.get(value, ('gray', 'black'))
                    self.dynamic_tiles[(i, j)].config(bg=bg_color)
                    self.dynamic_labels[(i, j)].config(text=f"{value}" if value else "", bg=bg_color, fg=fg_color)

        if moved_or_merged:
            self.add_new_tile()

        self.score_label.config(text=f"Score: {self.score}")

    def move_tiles_up(self, event):
        moved_or_merged = False
        for j in range(4):
            # Extract the current column values.
            current_column = [int(self.dynamic_labels[(i, j)].cget("text") or 0) for i in range(4)]

            # Consolidate non-zero tiles upwards.
            consolidated = [value for value in current_column if value != 0]
            new_column = []
            skip_next = False

            # Merge tiles from top to bottom.
            for k in range(len(consolidated)):
                if skip_next:
                    skip_next = False
                    continue
                if k < len(consolidated) - 1 and consolidated[k] == consolidated[k + 1]:
                    new_column.append(consolidated[k] * 2)
                    self.score += consolidated[k] * 2
                    moved_or_merged = True
                    skip_next = True  # Skip the next value since it's merged.
                else:
                    new_column.append(consolidated[k])

            # Fill the rest of the column with zeros (empty spaces).
            new_column.extend([0] * (4 - len(new_column)))

            # Update GUI if there's a change.
            for i, value in enumerate(new_column):
                if current_column[i] != value:
                    moved_or_merged = True
                    bg_color, fg_color = self.tile_colors.get(value, ('gray', 'black'))
                    self.dynamic_tiles[(i, j)].config(bg=bg_color)
                    self.dynamic_labels[(i, j)].config(text=f"{value}" if value else "", bg=bg_color, fg=fg_color)

        if moved_or_merged:
            self.add_new_tile()

        self.score_label.config(text=f"Score: {self.score}")

    def move_tiles_down(self, event):
        moved_or_merged = False
        for j in range(4):
            # Extract the current column values.
            current_column = [int(self.dynamic_labels[(i, j)].cget("text") or 0) for i in range(4)]

            # Consolidate non-zero tiles downwards by reversing the column for processing.
            consolidated = [value for value in current_column if value != 0]
            new_column = []
            skip_next = False

            # Merge tiles from bottom to top, working through the reversed list.
            for k in range(len(consolidated) - 1, -1, -1):
                if skip_next:
                    skip_next = False
                    continue
                if k > 0 and consolidated[k] == consolidated[k - 1]:
                    new_column.insert(0, consolidated[k] * 2)  # Insert at start to keep reversed order.
                    self.score += consolidated[k] * 2
                    moved_or_merged = True
                    skip_next = True  # Skip the next (technically previous) value since it's merged.
                else:
                    new_column.insert(0, consolidated[k])

            # Fill the rest of the column with zeros (empty spaces) at the start (top).
            new_column = [0] * (4 - len(new_column)) + new_column

            # Update GUI if there's a change.
            for i, value in enumerate(new_column):
                if current_column[i] != value:
                    moved_or_merged = True
                    bg_color, fg_color = self.tile_colors.get(value, ('gray', 'black'))
                    self.dynamic_tiles[(i, j)].config(bg=bg_color)
                    self.dynamic_labels[(i, j)].config(text=f"{value}" if value else "", bg=bg_color, fg=fg_color)

        if moved_or_merged:
            self.add_new_tile()

        self.score_label.config(text=f"Score: {self.score}")


if __name__ == "__main__":
    game = game()
    game.start_game()
    game.mainloop()

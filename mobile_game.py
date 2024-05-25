# Import libraries
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from ipywidgets import widgets, Button, HBox, VBox, Layout, Output
from IPython.display import clear_output, display

"""
This class sets up a N-Queens Game interface. 
"""


class N_Queens_Game:
    def __init__(self):
        # Flag for "AI" Queens
        self.start = True
        # Display "AI-Queens" on bootup
        self.positions = {
            (10, 2),
            (9, 2),
            (8, 2),
            (7, 2),
            (6, 2),
            (5, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 6),
            (8, 6),
            (9, 6),
            (10, 6),
            (8, 5),
            (8, 4),
            (8, 3),
            (10, 9),
            (10, 10),
            (10, 11),
            (10, 12),
            (10, 13),
            (9, 11),
            (8, 11),
            (7, 11),
            (6, 11),
            (5, 11),
            (4, 11),
            (4, 10),
            (4, 9),
            (4, 12),
            (4, 13),
        }

        # Initialize interactive matplotlib figure for N-Queens Game
        with plt.ioff():
            self.fig, self.ax = plt.subplots(figsize=(3.5, 3.5))
            self.fig.canvas.toolbar_visible = False
            self.fig.canvas.header_visible = False
            self.fig.canvas.footer_visible = False
            self.ax.axis("off")
            self.fig.canvas.mpl_connect(
                "button_press_event", self.onclick
            )  # For recording mouse click

        # Game stats
        self.step_number = 0
        self.queen_placement = len(self.positions)
        self.backtracking = 0

        # Game characteristics
        self.n = 16
        self.hint = False

        # Widgets for displaying the Game stats
        self.steps = widgets.Label(
            value=f"Total Steps: {self.step_number}",
            layout=widgets.Layout(margin="0 0 0 18px"),
        )
        self.backtracks = widgets.Label(
            value=f"Total Backtracking Steps: {self.backtracking}",
            layout=widgets.Layout(margin="0 0 0 18px"),
        )
        self.placements = widgets.Label(
            value=f"Total Queen Placements: {self.queen_placement}",
            layout=widgets.Layout(margin="0 0 0 18px"),
        )
        self.solution = widgets.HTML(
            value="",
            layout=widgets.Layout(margin="10px 0 0 50px"),
            style={"color": "#769656"},
        )

        # Widget for title
        self.title = widgets.Label(
            value="N-Queens Playground",
            style={"font_weight": "bold", "font_size": "20px"},
            layout=widgets.Layout(margin="10px 0 0px 0px"),
        )

        # Widget for user-input of size N
        self.size = widgets.IntSlider(
            value=self.n,
            min=4,
            max=16,
            step=1,
            description="Size of N:",
            style={"font_size": "15px"},
            layout=widgets.Layout(width="250px", margin="20px 0 0 5px"),
        )

        # Output area for game board fig and user controls
        self.output = Output()

        # Display the initial game board fig
        self.visualize_board()

    def setup(self):
        # Reset button for the game
        self.reset = Button(description="New")
        self.reset.on_click(self.new_reset)

        self.hint_check = widgets.Checkbox(value=False, indent=False)
        hint_label = widgets.Label(
            "Hint", layout=Layout(margin="0px 0 0 -285px", width="auto")
        )
        self.hint_widget = HBox(
            [self.hint_check, hint_label],
            layout=Layout(width="100%", margin="2.5px 0 0 20px"),
        )

        self.ai_check = widgets.Checkbox(value=False, indent=False)
        ai_label = widgets.Label(
            "AI", layout=Layout(margin="0px 0 0 -285px", width="auto")
        )
        self.ai_widget = HBox(
            [self.ai_check, ai_label],
            layout=Layout(width="100%", margin="2.5px 0 0 -545px"),
        )

        # Linking the observe method to the checkbox widgets
        self.hint_check.observe(self.observe_hint, names="value")
        self.ai_check.observe(self.observe_ai, names="value")

        # Combine reset button and hint checkbox horizontally
        button_row = HBox(
            [self.reset, self.hint_widget, self.ai_widget],
            layout=Layout(margin="20px 0px 5px 25px"),
        )

        # Combine game stats widgets vertically
        stats_box = VBox(
            [
                self.steps,
                self.placements,
                self.backtracks,
                self.solution,
            ],
            layout=Layout(margin="10px"),
        )

        # Combine all above widgets vertically for user control game panel
        user_control = VBox(
            [self.size, button_row, stats_box], layout=Layout(margin="0 0 0 55px")
        )

        # Store title into a box for shifting position
        title = VBox([self.title], layout=Layout(margin="47.5px 0 5px 75px"))

        # Combine board game fig and user control game panel horizontally
        with self.output:
            clear_output(wait=True)  # Clear the previous output
            display(
                VBox(
                    [
                        title,  # Add title above the figure
                        self.fig.canvas,  # Game board fig
                        user_control,  # User control panel
                    ],
                    layout=Layout(margin="-47.5px 0px 0 0px"),
                )
            )

        # Display the output / game
        display(self.output)

    # Update game board fig when hint checkbox is changed
    def observe_hint(self, change):
        self.hint = change["new"]
        self.visualize_board()

    # Observe AI checkbox
    def observe_ai(self, change):
        if change["new"]:
            self.start_ai_solver()

    # Reset game stats and game board fig
    def new_reset(self, change=None):
        # Switch start flag to false
        self.start = False

        self.n = self.size.value
        self.positions.clear()
        self.step_number = 0
        self.backtracking = 0
        self.queen_placement = 0
        self.solution.value = ""
        self.steps.value = f"Total Steps: {self.step_number}"
        self.placements.value = f"Total Queen Placements: {self.queen_placement}"
        self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
        self.ai_check.value = False

        self.visualize_board()

    # Function for drawing the N-Queens game board states
    def visualize_board(self):

        board = np.zeros((self.n, self.n))  # Initialize board structure
        board[1::2, ::2] = 1  # Dark/Green squares
        board[::2, 1::2] = 1  # Dark/Green squares
        queen_img = plt.imread("queen.png")  # Load queen image piece

        zoom_factor = 0.05 * 6 / self.n  # Adjust size of queen image piece

        self.ax.clear()  # Clear axis

        # Color the chessboard with light and dark squares
        for y in range(self.n):
            for x in range(self.n):
                # Light squares (0): beige; Dark squares (1): green
                color = "#769656" if board[y, x] == 1 else "#eeeed2"
                self.ax.fill_between(
                    [x, x + 1], y, y + 1, color=color, edgecolor="none"
                )

        # Draw the Queen image piece on the board
        for y, x in self.positions:
            img = OffsetImage(queen_img, zoom=zoom_factor)
            # Creates an annotation box for Queen placement
            ab = AnnotationBbox(
                img, (x + 0.5, y + 0.5), frameon=False, boxcoords="data", pad=0
            )
            self.ax.add_artist(ab)

        # Set plot parameters
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        title_font = {"fontsize": 10}
        if self.start:
            self.ax.set_title("AI-Queens", fontdict=title_font)
        else:
            self.ax.set_title(f"{self.n}-Queens", fontdict=title_font)
        self.ax.invert_yaxis()

        # Adjust subplot parameters to remove white space
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Print threats values on game board if hint is checked
        if self.hint:
            for y in range(self.n):
                for x in range(self.n):
                    # Write threats value for empty spots on the board
                    if (y, x) not in self.positions:
                        threat = self.compute_threats(y, x)
                        # 0 threats in green meaning safe spot; otherwise, red
                        color = "green" if threat == 0 else "red"
                        self.ax.text(
                            x + 0.5,
                            y + 0.5,
                            str(threat),
                            fontsize=8,
                            ha="center",
                            va="center",
                            color=color,
                        )

    # Compute threats value for a spot given row and co
    def compute_threats(self, row, col):
        threats = 0
        for y, x in self.positions:
            # Cannot share row, col, diagonals in both directions
            if y == row or x == col or abs(y - row) == abs(x - col):
                threats += 1
        return threats

    # Track mouse click events for gameplay
    def onclick(self, event):
        # When a click is detected
        if (
            event.inaxes is not None
            and event.xdata is not None
            and event.ydata is not None
        ):
            # Convert click coordinates to board row and col
            row, col = int(event.ydata), int(event.xdata)

            # If the clicked spot is a safe spot
            if (row, col) not in self.positions and self.compute_threats(row, col) == 0:
                self.positions.add((row, col))
                self.queen_placement += 1
                self.step_number += 1
            elif (row, col) in self.positions:  # backtrack if clicked on occupied spot
                self.positions.remove((row, col))
                self.backtracking += 1
                self.step_number += 1

            # When clicked an unsafe spot, nothing happens

            # Update stats and draw the new board
            self.steps.value = f"Total Steps: {self.step_number}"
            self.placements.value = f"Total Queen Placements: {self.queen_placement}"
            self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
            self.visualize_board()

            # If a solution is found
            if len(self.positions) == self.n:
                self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
            else:
                self.ai_check.value = False
                self.solution.value = ""

    def count_safe_spots_for_board(self, row, col):
        board_copy = [r[:] for r in self.board]
        board_copy[row][col] = 1  # Place the Queen hypothetically
        safe_spots = 0
        for r in range(self.n):
            for c in range(self.n):
                if self.is_safe(board_copy, r, c):
                    safe_spots += 1
        return safe_spots

    def is_safe(self, board, row, col):
        for i in range(self.n):
            if board[i][col] == 1 and i != row:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, self.n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, self.n, 1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, self.n, 1), range(col, self.n, 1)):
            if board[i][j] == 1:
                return False
        return True

    def update_threats(self, threats, row, col):
        threats[row][col] += 1
        for i in range(row):
            threats[i][col] += 1
        for i in range(row + 1, self.n):
            threats[i][col] += 1
        for j in range(col):
            threats[row][j] += 1
        for j in range(col + 1, self.n):
            threats[row][j] += 1
        for i, j in zip(range(row + 1, self.n), range(col - 1, -1, -1)):
            threats[i][j] += 1
        for i, j in zip(range(row + 1, self.n), range(col + 1, self.n)):
            threats[i][j] += 1
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            threats[i][j] += 1
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, self.n, 1)):
            threats[i][j] += 1

    def backtrack_threats(self, threats, row, col):
        threats[row][col] -= 1
        for i in range(row):
            threats[i][col] -= 1
        for i in range(row + 1, self.n):
            threats[i][col] -= 1
        for j in range(col):
            threats[row][j] -= 1
        for j in range(col + 1, self.n):
            threats[row][j] -= 1
        for i, j in zip(range(row + 1, self.n), range(col - 1, -1, -1)):
            threats[i][j] -= 1
        for i, j in zip(range(row + 1, self.n), range(col + 1, self.n)):
            threats[i][j] -= 1
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            threats[i][j] -= 1
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, self.n, 1)):
            threats[i][j] -= 1

    def look_ahead(self, threats, row):
        safe = False
        for j in range(self.n):
            if threats[row][j] == 0:
                safe = True
                break
        return safe

    def arc_consistency(self, row):
        prune = []
        row_threats = self.threats[row]
        used_rows_copy = self.used_rows.copy()
        used_rows_copy.add(row)
        safe_cols = [index for index, threats in enumerate(row_threats) if threats == 0]
        for j in safe_cols:
            threats_copy = [r[:] for r in self.threats]
            self.update_threats(threats_copy, row, j)
            for i in range(self.n):
                if i not in used_rows_copy:
                    if not self.look_ahead(threats_copy, i):
                        prune.append(j)
                        break
        return prune

    def find_row_with_mrv(self):
        mrv = float("inf")
        mrv_row = None
        for row in range(self.n):
            if row not in self.used_rows:
                row_threats = self.threats[row]
                safe_cols = [
                    index for index, threats in enumerate(row_threats) if threats == 0
                ]
                safe_spots = len(safe_cols)
                if safe_spots < mrv:
                    mrv = safe_spots
                    mrv_row = row
        return mrv_row

    def solve_n_queens_util(self):
        if len(self.used_rows) == self.n:
            return True
        mrv_row = self.find_row_with_mrv()
        prune = self.arc_consistency(mrv_row)
        col_lcv = []
        for col in range(self.n):
            if self.is_safe(self.board, mrv_row, col):
                lcv = self.count_safe_spots_for_board(mrv_row, col)
                col_lcv.append((col, lcv))
        col_lcv.sort(key=lambda x: x[1])
        for col, _ in col_lcv:
            if col not in prune:
                self.board[mrv_row][col] = 1
                self.update_threats(self.threats, mrv_row, col)
                self.positions.add((mrv_row, col))
                self.used_rows.add(mrv_row)
                self.step_number += 1
                self.queen_placement += 1
                if self.solve_n_queens_util():
                    return True
                self.board[mrv_row][col] = 0
                self.backtrack_threats(self.threats, mrv_row, col)
                self.positions.remove((mrv_row, col))
                self.used_rows.remove(mrv_row)
                self.step_number += 1
                self.backtracking += 1
        return False

    def solve(self):
        # Initialize the board with zeros and place the existing queens
        self.board = [[0] * self.n for _ in range(self.n)]
        for r, c in self.positions:
            self.board[r][c] = 1

        # Initialize threats and used rows based on current positions
        self.update_threats_matrix()  # Assuming update_threats_matrix populates self.threats
        self.used_rows = set(r for (r, c) in self.positions)

        # Set the initial counters based on the existing setup
        # self.step_number = 0
        # self.queen_placement = len(self.positions)
        # self.backtracking = 0

        # Run the utility solver
        if not self.solve_n_queens_util():
            # If no solution found from the current state, clear and start over
            self.positions.clear()
            self.used_rows.clear()
            self.board = [[0] * self.n for _ in range(self.n)]
            self.threats = [[0] * self.n for _ in range(self.n)]
            self.solve_n_queens_util()

        self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
        self.visualize_board()

    def update_threats_matrix(self):
        # Initialize the threats matrix with zeros
        self.threats = [[0] * self.n for _ in range(self.n)]

        # Compute threats for each cell based on current positions
        for r, c in self.positions:
            self.update_threats(self.threats, r, c)

    def update_threats(self, threats, row, col):
        # Increment threats for all affected cells by placing a queen at (row, col)
        for i in range(self.n):
            # Same row and column
            threats[row][i] += 1
            threats[i][col] += 1
            # Diagonals
            if row + i < self.n and col + i < self.n:
                threats[row + i][col + i] += 1
            if row - i >= 0 and col - i >= 0:
                threats[row - i][col - i] += 1
            if row + i < self.n and col - i >= 0:
                threats[row + i][col - i] += 1
            if row - i >= 0 and col + i < self.n:
                threats[row - i][col + i] += 1
        threats[row][col] -= 3  # Remove overcounted threats for the queen's own cell

    def start_ai_solver(self):
        self.solve()
        self.steps.value = f"Total Steps: {self.step_number}"
        self.placements.value = f"Total Queen Placements: {self.queen_placement}"
        self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
        if len(self.positions) == self.n:
            self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
        else:
            self.solution.value = ""

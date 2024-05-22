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
            self.fig, self.ax = plt.subplots(figsize=(3, 3))
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
        self.solution = widgets.Label(
            value="",
            layout=widgets.Layout(margin="0 0 0 18px"),
        )

        # Widget for title
        self.title = widgets.Label(
            value="N-Queens Playground",
            style={"font_weight": "bold", "font_size": "15px"},
            layout=widgets.Layout(margin="0 0 0 15px"),
        )

        # Widget for user-input of size N
        self.size = widgets.BoundedIntText(
            value=self.n,
            min=4,
            max=16,
            step=1,
            description="Size of N:",
            style={"font_size": "15px"},
            layout=widgets.Layout(width="200px", margin="10px 0 0 5px"),
        )

        # Output area for game board fig and user controls
        self.output = Output()

        # Display the initial game board fig
        self.visualize_board()

    def setup(self):
        # Reset button for the game
        self.reset = Button(description="New")
        self.reset.on_click(self.new_reset)

        # Checkbox for hint of the game
        self.hint_check = widgets.Checkbox(
            value=False,
            description="Hint",
            indent=False,
            layout=Layout(margin="5px 0px 0 15px"),
        )

        # Observe hint checkbox value and update board game fig
        self.hint_check.observe(self.observe_hint, names="value")

        # Combine reset button and hint checkbox horizontally
        button_row = HBox(
            [self.reset, self.hint_check],
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
            [self.size, button_row, stats_box], layout=Layout(margin="0 0 0 35px")
        )

        # Store title into a box for shifting position
        title = VBox([self.title], layout=Layout(margin="40px 0 0 60px"))

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
                    layout=Layout(margin="0px 0px 0 25px"),
                )
            )

        # Display the output / game
        display(self.output)

    # Update game board fig when hint checkbox is changed
    def observe_hint(self, change):
        self.hint = change["new"]
        self.visualize_board()

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

        self.visualize_board()

    # Function for drawing the N-Queens game board states
    def visualize_board(self):

        board = np.zeros((self.n, self.n))  # Initialize board structure
        board[1::2, ::2] = 1  # Dark/Green squares
        board[::2, 1::2] = 1  # Dark/Green squares
        queen_img = plt.imread("queen.png")  # Load queen image piece

        zoom_factor = 0.05 * 5 / self.n  # Adjust size of queen image piece

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
                self.solution.value = "Solution Found!"

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
            layout=widgets.Layout(margin="10px 0 0px px"),
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
                self.solution.value = ""


"""
This module sets up the visualization tool and runs the N-Queens Solver based on
user input for size (N) and methods (Algorithm + Ordering + Filtering).
"""

# Import libraries
import ipywidgets as widgets
from IPython.display import clear_output, display

# Import N-Queens Solvers
from base import N_Queens_Solver

# Ordering
from mrv import N_Queens_Solver_MRV
from lcv import N_Queens_Solver_LCV
from mrv_lcv import N_Queens_Solver_MRV_LCV

# Filtering
from fc import N_Queens_Solver_FC
from ac import N_Queens_Solver_AC

# Ordering + Forward Checking
from mrv_fc import N_Queens_Solver_MRV_FC
from lcv_fc import N_Queens_Solver_LCV_FC
from mrv_lcv_fc import N_Queens_Solver_MRV_LCV_FC

# Ordering + Arc Consistency
from mrv_ac import N_Queens_Solver_MRV_AC
from lcv_ac import N_Queens_Solver_LCV_AC
from mrv_lcv_ac import N_Queens_Solver_MRV_LCV_AC


# Sets up visualization tool to run the N-Queens Solver
def N_Queens_Solver_Vis():

    title = widgets.Label(
        value="Custom N-Queens Solver",
        style={"font_weight": "bold", "font_size": "20px"},
        layout=widgets.Layout(margin="0 0 0 70px"),
    )

    # User input size N for chessboard
    size = widgets.BoundedIntText(
        value=8,
        min=4,
        max=32,
        step=1,
        description="Size of N:",
        layout=widgets.Layout(width="200px", margin="10px 0 10px 50px"),
    )

    # Dropdown list for algorithm options
    algorithm_opt = widgets.RadioButtons(
        options=["Backtracking"],
        description="Algorithm:",
        layout=widgets.Layout(margin="0 0 0 72px"),
    )

    # Dropdown list for ordering options
    ordering_opt = widgets.RadioButtons(
        options=["None", "MRV", "LCV", "MRV + LCV"],
        description="Ordering:",
        layout=widgets.Layout(margin="8px 0 0 72px"),
    )

    # Dropdown list for filtering options
    filtering_opt = widgets.RadioButtons(
        options=["None", "Forward Checking", "Arc Consistency"],
        description="Filtering:",
        layout=widgets.Layout(margin="0 0 0 72px"),
    )

    # Click button to run the N-Queens Solver
    solve_button = widgets.Button(
        description="Solve N-Queens", layout=widgets.Layout(margin="8px 0 8px 72px")
    )

    # Split the output area into left and right
    left_output_area = widgets.Output()
    right_output_area = widgets.Output()

    # Combine all widgets above vertically in list order for left output area
    left_box = widgets.VBox(
        [
            title,
            size,
            algorithm_opt,
            ordering_opt,
            filtering_opt,
            solve_button,
            left_output_area,
        ]
    )

    # Define widget in vertical list order for right output area
    right_box = widgets.VBox([right_output_area])

    # Define widget for image display area
    img_output_area = widgets.Output()

    # Define function to run the N-Queens Solver when solve_button is clicked
    def click_solve_button(b):

        # Display for left output area (under solve_button)
        with left_output_area:
            clear_output(wait=True)  # Clear the output area before display
            n = size.value  # User input for N
            algorithm = algorithm_opt.value  # User input for algorithm
            ordering = ordering_opt.value  # User input for ordering
            filtering = filtering_opt.value  # User input for filtering

            # Start solving
            print(f"        Finding Solution to {n}-Queens...")
            print()

            # Initialize N-Queens Solver based on user input (no visualization)
            # Baseline
            if (
                algorithm == "Backtracking"
                and ordering == "None"
                and filtering == "None"
            ):
                solver_no_vis = N_Queens_Solver(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # MRV
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV"
                and filtering == "None"
            ):
                solver_no_vis = N_Queens_Solver_MRV(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # LCV
            elif (
                algorithm == "Backtracking"
                and ordering == "LCV"
                and filtering == "None"
            ):
                solver_no_vis = N_Queens_Solver_LCV(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # MRV + LCV
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV + LCV"
                and filtering == "None"
            ):
                solver_no_vis = N_Queens_Solver_MRV_LCV(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # Forward Checking
            elif (
                algorithm == "Backtracking"
                and ordering == "None"
                and filtering == "Forward Checking"
            ):
                solver_no_vis = N_Queens_Solver_FC(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # Arc Consistency
            elif (
                algorithm == "Backtracking"
                and ordering == "None"
                and filtering == "Arc Consistency"
            ):
                solver_no_vis = N_Queens_Solver_AC(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # MRV + Forward Checking
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV"
                and filtering == "Forward Checking"
            ):
                solver_no_vis = N_Queens_Solver_MRV_FC(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # LCV + Forward Checking
            elif (
                algorithm == "Backtracking"
                and ordering == "LCV"
                and filtering == "Forward Checking"
            ):
                solver_no_vis = N_Queens_Solver_LCV_FC(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # MRV + LCV + Forward Checking
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV + LCV"
                and filtering == "Forward Checking"
            ):
                solver_no_vis = N_Queens_Solver_MRV_LCV_FC(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # MRV + Arc Consistency
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV"
                and filtering == "Arc Consistency"
            ):
                solver_no_vis = N_Queens_Solver_MRV_AC(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # LCV + Arc Consistency
            elif (
                algorithm == "Backtracking"
                and ordering == "LCV"
                and filtering == "Arc Consistency"
            ):
                solver_no_vis = N_Queens_Solver_LCV_AC(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )
            # MRV + LCV + Arc Consistency
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV + LCV"
                and filtering == "Arc Consistency"
            ):
                solver_no_vis = N_Queens_Solver_MRV_LCV_AC(
                    img_output_area,
                    progress_bar=None,
                    progress_label=None,
                    vis=False,
                    num_img=0,
                    size=n,
                )

            # Run the N-Queens Sovler with no visualization first
            solver_no_vis.solve()
            print("        Solution Found:")

            # Output solution display
            if solver_no_vis.positions:
                # Print four solution coordinates on each line
                for i, position in enumerate(solver_no_vis.positions):
                    end_char = "\n" if (i + 1) % 4 == 0 else " "
                    if i % 4 == 0:
                        print("       ", end=" ")
                    print(position, end=end_char)

                # Print extra new lines
                if len(solver_no_vis.positions) % 4 != 0:
                    print()
                print()

                # Print solution metrics
                print(f"        Total Steps: {solver_no_vis.step_number}")
                print(
                    f"        Total Queen Placements: "
                    f"{solver_no_vis.queen_placement}"
                )
                print(
                    f"        Total Backtracking Steps: "
                    f"{solver_no_vis.backtracking}"
                )
            else:
                print("        No solution exists.")

        # Display for right output area
        with right_output_area:
            clear_output(wait=True)  # Clear the output area before display

            print("Generating Visualization...")

            # Threshold for saving last max_img step images for visualization
            max_img = (
                10 if solver_no_vis.step_number > 10 else solver_no_vis.step_number
            )

            # Progress bar for tracking visualization generation
            progress_bar = widgets.IntProgress(
                value=0,
                min=0,
                max=max_img,
                description="Progress:",
                layout=widgets.Layout(width="200px"),
            )

            # Progress label for status of visualization generation
            progress_label = widgets.Label("0% Complete")

            # Combine progress bar and label horizontally in list order
            progress_box = widgets.HBox(
                [progress_bar, progress_label],
                layout=widgets.Layout(margin="0 0 0 -20px"),
            )

            # Display progress bar
            display(progress_box)

            # Extract user input
            n = size.value  # User input for N
            algorithm = algorithm_opt.value  # User input for algorithm
            ordering = ordering_opt.value  # User input for ordering
            filtering = filtering_opt.value  # User input for filtering

            # Initialize N-Queens Solver based on user input (w/ visualization)
            # Baseline
            if (
                algorithm == "Backtracking"
                and ordering == "None"
                and filtering == "None"
            ):
                solver_vis = N_Queens_Solver(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # MRV
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV"
                and filtering == "None"
            ):
                solver_vis = N_Queens_Solver_MRV(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # LCV
            elif (
                algorithm == "Backtracking"
                and ordering == "LCV"
                and filtering == "None"
            ):
                solver_vis = N_Queens_Solver_LCV(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # MRV + LCV
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV + LCV"
                and filtering == "None"
            ):
                solver_vis = N_Queens_Solver_MRV_LCV(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # Forward Checking
            elif (
                algorithm == "Backtracking"
                and ordering == "None"
                and filtering == "Forward Checking"
            ):
                solver_vis = N_Queens_Solver_FC(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # Arc Consistency
            elif (
                algorithm == "Backtracking"
                and ordering == "None"
                and filtering == "Arc Consistency"
            ):
                solver_vis = N_Queens_Solver_AC(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # MRV + Forward Checking
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV"
                and filtering == "Forward Checking"
            ):
                solver_vis = N_Queens_Solver_MRV_FC(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # LCV + Forward Checking
            elif (
                algorithm == "Backtracking"
                and ordering == "LCV"
                and filtering == "Forward Checking"
            ):
                solver_vis = N_Queens_Solver_LCV_FC(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # MRV + LCV + Forward Checking
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV + LCV"
                and filtering == "Forward Checking"
            ):
                solver_vis = N_Queens_Solver_MRV_LCV_FC(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # MRV + Arc Consistency
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV"
                and filtering == "Arc Consistency"
            ):
                solver_vis = N_Queens_Solver_MRV_AC(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # LCV + Arc Consistency
            elif (
                algorithm == "Backtracking"
                and ordering == "LCV"
                and filtering == "Arc Consistency"
            ):
                solver_vis = N_Queens_Solver_LCV_AC(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )
            # MRV + LCV + Arc Consistency
            elif (
                algorithm == "Backtracking"
                and ordering == "MRV + LCV"
                and filtering == "Arc Consistency"
            ):
                solver_vis = N_Queens_Solver_MRV_LCV_AC(
                    img_output_area,
                    progress_bar,
                    progress_label,
                    vis=True,
                    num_img=solver_no_vis.step_number,
                    size=n,
                )

            # Run the N-Queens Solver with visualization
            solver_vis.solve()

            # User control for visualization tool
            # Slider for updating image steps
            slider = widgets.IntSlider(
                min=0,
                max=max_img,
                step=1,
                value=0,
                layout=widgets.Layout(width="180px"),
            )

            # Play button for automatically displaying image steps in sequence
            play = widgets.Play(min=0, max=max_img, step=1, interval=500)

            # Link the value for play button and slider
            widgets.jslink((play, "value"), (slider, "value"))

            # Previous and next button for updating image steps by one
            prev_button = widgets.Button(description="Previous")
            next_button = widgets.Button(description="Next")

            # Helper Function for visualization tool
            # Display the updated image step based on user button control
            def update_image(change):
                solver_vis.display_figure(change["new"])

            # Define function to update play value when prev_button is clicked
            def click_prev_button(b):
                if play.value > 0:
                    play.value -= 1

            # Define function to update play value when next_button is clicked
            def click_next_button(b):
                if play.value < play.max:
                    play.value += 1

            # Link buttons to trigger function events when clicked
            prev_button.on_click(click_prev_button)
            next_button.on_click(click_next_button)

            # Combine previous and next button horizontally for display
            buttons_box = widgets.HBox(
                [prev_button, next_button], layout=widgets.Layout(margin="0 0 0 50px")
            )

            # Observe play's value as it is changed and update image step
            play.observe(update_image, names="value")

            # Wrap play into horizontal widget box with slider
            play_box = widgets.HBox(
                [play, slider], layout=widgets.Layout(margin="10px 0 0 50px")
            )

            # Combine play, prev, next button and img output vertically
            right_box = widgets.VBox(
                [buttons_box, play_box, img_output_area],
                layout=widgets.Layout(overflow="hidden", margin="20px 0 0 -20px"),
            )

            # Display for right output area
            display(right_box)

            # Initialize first image step for display
            solver_vis.display_figure(0)

    # Link solve button to trigger function events (run solver) when clicked
    solve_button.on_click(click_solve_button)

    # Combine both left and right output area horizontally and display
    layout_box = widgets.VBox([left_box, right_box])
    display(layout_box)

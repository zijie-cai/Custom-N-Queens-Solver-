import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from ipywidgets import widgets, Button, HBox, VBox, Layout, Output, Dropdown
from IPython.display import clear_output, display
import asyncio
import random
from IPython.display import Audio
from IPython.display import display, HTML, Javascript
import matplotlib.patches as patches
import math


class N_Queens_Game:
    def __init__(self):

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

        with plt.ioff():
            self.fig, self.ax = plt.subplots(figsize=(3.5, 3.5))
            self.fig.canvas.toolbar_visible = False
            self.fig.canvas.header_visible = False
            self.fig.canvas.footer_visible = False
            self.ax.axis("off")
            self.fig.canvas.mpl_connect("button_press_event", self.onclick)

        self.step_number = 0
        self.queen_placement = 0
        self.backtracking = 0
        self.n = 16
        self.hint = False
        self.ai = False

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
        self.title = widgets.Button(
            description="N-Queens Playground",  # Use 'description' instead of 'value' for buttons
            button_style="",  # Optional: styles like 'success', 'info', 'warning', 'danger', or ''
            style={
                "button_color": "transparent",
                "font_weight": "bold",
                "font_size": "20px",
            },  # Apply text styling here
            layout=widgets.Layout(
                margin="10px 0px 0px -75px", width="250px", align_self="center"
            ),  # Adjust layout as needed
        )
        self.title.on_click(self.title_click)  # Define a method to handle click events

        self.size = widgets.IntSlider(
            value=self.n,
            min=4,
            max=16,
            step=1,
            description="Size of N:",
            style={"font_size": "15px"},
            layout=widgets.Layout(width="250px", margin="20px 0 0 5px"),
        )

        self.output = Output()
        display(self.output)

    def title_click(self, b):
        self.create_solver_menu_ui()

    def setup(self):
        self.reset = Button(description="New", layout=Layout(width="120px"))
        self.reset.on_click(self.new_reset)

        self.hint_check = widgets.Checkbox(value=False, indent=False)
        hint_label = widgets.Label("Hint", layout=Layout(margin="0px 0 0 -281px"))
        self.hint_widget = HBox(
            [self.hint_check, hint_label],
            layout=Layout(width="100%", margin="2.5px 0 0 24px", overflow="hidden"),
        )

        self.ai_check = widgets.Checkbox(value=False, indent=False)
        self.ai_label = widgets.Button(
            description="AI",
            layout=widgets.Layout(width="auto", margin="-0.5px 0 0 -290px"),
            style={
                "button_color": "transparent",
                "font_size": "12.5px",
            },
        )

        self.ai_label.add_class("button-style")
        self.ai_widget = HBox(
            [self.ai_check, self.ai_label],
            layout=Layout(width="100%", margin="2px 0 0 -68px", overflow="hidden"),
        )

        self.ai_label.on_click(self.on_ai_click)
        self.hint_check.observe(self.observe_hint, names="value")
        self.ai_check.observe(self.observe_ai, names="value")

        button_row = HBox(
            [self.reset, self.hint_widget, self.ai_widget],
            layout=Layout(margin="20px 0px 5px 25px", width="300px"),
        )
        stats_box = VBox(
            [self.steps, self.placements, self.backtracks, self.solution],
            layout=Layout(margin="10px"),
        )
        self.user_control = VBox(
            [self.size, button_row, stats_box],
            layout=Layout(margin="0 0 0 75px", overflow="hidden", align_self="center"),
        )
        self.title = VBox([self.title], layout=Layout(margin="35px 0 10px 75px"))

        self.canvas = VBox(
            [self.fig.canvas],
            layout=Layout(margin="0px 0 0px 0px", align_self="center"),
        )

        self.create_solver_config_ui()
        self.create_solver_menu_ui()

        # display(self.output)
        # css = """
        # <style>
        # .button-style {
        #     text-decoration: underline;
        # }
        # </style>
        #    """
        # with self.output:
        #  clear_output(wait=True)
        #   display(HTML(css))
        #   display(
        #       VBox(
        #           [self.title, self.fig.canvas, self.user_control],
        #           layout=Layout(margin="-47.5px 0px 0 0px"),
        #       )
        #  )
        #  self.visualize_board()
        #   self.fig.canvas.draw()

    def observe_hint(self, change):
        self.hint = change["new"]
        self.visualize_board()
        self.fig.canvas.draw()

    def observe_ai(self, change):
        self.ai = change["new"]
        if self.ai:
            asyncio.create_task(self.start_ai_solver())

    def new_reset(self, change=None):

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
        self.fig.canvas.draw()

    def visualize_board(self):
        board = np.zeros((self.n, self.n))
        board[1::2, ::2] = 1
        board[::2, 1::2] = 1
        queen_img = plt.imread("queen.png")
        zoom_factor = 0.05 * 6 / self.n

        self.ax.clear()
        for y in range(self.n):
            for x in range(self.n):
                color = "#769656" if board[y, x] == 1 else "#eeeed2"
                self.ax.fill_between(
                    [x, x + 1], y, y + 1, color=color, edgecolor="none"
                )

        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        # Optionally, add grid lines
        self.ax.set_xticks([i for i in range(self.n + 1)])
        self.ax.set_yticks([i for i in range(self.n + 1)])
        self.ax.grid(which="both", color="black", linestyle="-", linewidth=0.5)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_aspect("equal")
        self.ax.invert_yaxis()
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        if self.hint:
            # Optionally, add grid lines
            self.ax.set_xticks([i for i in range(self.n + 1)])
            self.ax.set_yticks([i for i in range(self.n + 1)])
            self.ax.grid(which="both", color="black", linestyle="-", linewidth=0.5)
            self.ax.set_xticklabels([])
            self.ax.set_yticklabels([])
            self.ax.set_aspect("equal")

            max_threat = max(
                self.compute_threats(y, x) for y in range(self.n) for x in range(self.n)
            )

            for y in range(self.n):
                for x in range(self.n):

                    threat = self.compute_threats(y, x)
                    if threat == 0:
                        color = "#5ced73"  # Green for no threat
                    else:
                        # Calculate the intensity of red based on the threat level
                        intensity = 255 - int(255 * (threat / max_threat))
                        color = f"#FF{intensity:02X}{intensity:02X}"  # Gradient of red
                    self.ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

        for y, x in self.positions:
            img = OffsetImage(queen_img, zoom=zoom_factor)
            ab = AnnotationBbox(
                img, (x + 0.5, y + 0.5), frameon=False, boxcoords="data", pad=0
            )
            self.ax.add_artist(ab)

    def compute_threats(self, row, col):
        threats = 0
        for y, x in self.positions:

            if y == row or x == col or abs(y - row) == abs(x - col):
                threats += 1

            if (row, col) == (y, x):
                threats -= 1

        return threats

    def is_board_safe(self):
        """
        Check if the entire board is safe (no queens threaten each other).
        """

        for row1, col1 in self.positions:
            for row2, col2 in self.positions:
                if (row1, col1) != (row2, col2):
                    if (
                        row1 == row2
                        or col1 == col2
                        or abs(row1 - row2) == abs(col1 - col2)
                    ):
                        return False
        return True

    def find_most_conflict(self):
        most_conflict = (-1, -1)
        conflict = 0
        max = -1
        for row1, col1 in self.positions:
            for row2, col2 in self.positions:
                if (row1, col1) != (row2, col2):
                    if (
                        row1 == row2
                        or col1 == col2
                        or abs(row1 - row2) == abs(col1 - col2)
                    ):
                        conflict += 1
                if conflict > max:
                    max = conflict
                    most_conflict = (row1, col1)

        return most_conflict

    def count_conflicts(self):
        conflict = 0
        for row1, col1 in self.positions:
            for row2, col2 in self.positions:
                if (row1, col1) != (row2, col2):
                    if (
                        row1 == row2
                        or col1 == col2
                        or abs(row1 - row2) == abs(col1 - col2)
                    ):
                        conflict += 1
        return conflict

    def onclick(self, event):
        if event.inaxes and event.xdata is not None and event.ydata is not None:
            row, col = int(event.ydata), int(event.xdata)
            if (row, col) not in self.positions and len(self.positions) < (
                self.n * self.n
            ):
                self.positions.add((row, col))
                self.queen_placement += 1
                self.step_number += 1

            elif (row, col) in self.positions:
                self.positions.remove((row, col))
                self.backtracking += 1
                self.step_number += 1

            self.steps.value = f"Total Steps: {self.step_number}"
            self.placements.value = f"Total Queen Placements: {self.queen_placement}"
            self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"

            self.visualize_board()
            self.fig.canvas.draw()

            if len(self.positions) == self.n and self.count_conflicts() == 0:

                self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
            else:
                self.ai_check.value = False
                self.solution.value = ""

    async def start_ai_solver(self):
        await self.solve()

        self.steps.value = f"Total Steps: {self.step_number}"
        self.placements.value = f"Total Queen Placements: {self.queen_placement}"
        self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
        if len(self.positions) == self.n and self.count_conflicts() == 0:
            self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
        else:
            self.solution.value = ""

    def start_game(self, button):
        # Logic to start the game
        clear_output(wait=True)
        self.display_game_interface()

    def display_game_interface(self):
        display(self.output)
        css = """
            <style>
            .button-style { 
                text-decoration: underline;
            }
            </style>
            """
        with self.output:
            clear_output(wait=True)
            display(HTML(css))
            display(
                VBox(
                    [self.title, self.canvas, self.user_control],
                    layout=Layout(margin="-47.5px 0px 0 0px", width="875px"),
                )
            )
            self.visualize_board()
            self.fig.canvas.draw()

    def create_solver_menu_ui(self):

        author_info = widgets.HTML(
            value="<h3 style='color: gray;'>Created by Zijie Cai</h3>",
            layout=widgets.Layout(margin="-10px 0px -10px 0px", align_self="center"),
        )
        description = widgets.HTML(
            value="""
            <p style='text-align: justify; text-indent: 20px;'>
            Welcome to the N-Queens Playground! This interactive tool provides a dynamic visualization to help you solve the N-Queens puzzle. It features a step-by-step AI solver that employs Constraint Satisfaction Problem (CSP) algorithms and heuristics to place N queens on an NxN chessboard without any two queens threatening each other. Click the button below to configure the board and watch the solver in action!
            </p>
            """,
            layout=widgets.Layout(
                margin="0px 0 0px 0px", width="335px", align_self="center"
            ),
        )
        start_button = widgets.Button(
            description="Enter Playground",
            button_style="success",  # 'success', 'info', 'warning', 'danger' or ''
            style={"font_weight": "bold"},
            layout=widgets.Layout(
                width="200px",
                height="50px",
                align_self="center",
                margin="15px 0 0px 0px",
            ),
        )

        start_button.on_click(self.start_game)

        vbox = widgets.VBox(
            [self.title, author_info, description, start_button],
            layout=widgets.Layout(
                margin="75px 0px 0 0px",
                width="100%",  # Ensuring it doesn't exceed the width of its parent
                overflow="auto",
            ),
        )
        with self.output:
            clear_output(wait=True)
            display(vbox)

    def create_solver_config_ui(self):
        # Title for the configuration UI
        self.config_title = widgets.Label(
            value="AI CSP Solver Configuration",
            style={"font_weight": "bold", "font_size": "20px"},
            layout=widgets.Layout(
                margin="150px 0 10px 45px", align_self="center"
            ),  # Adjust top and bottom margin
        )

        self.algorithm_dropdown = Dropdown(
            options=["Backtracking"],
            value="Backtracking",
            description="Algorithm:",
            disabled=False,
            layout=widgets.Layout(margin="5px 0 5px 20px", align_self="center"),
        )

        self.ordering_dropdown = Dropdown(
            options=["None", "MRV", "LCV", "MRV + LCV"],
            value="MRV + LCV",
            description="Ordering:",
            disabled=False,
            layout=widgets.Layout(margin="5px 0 5px 20px", align_self="center"),
        )

        self.filtering_dropdown = Dropdown(
            options=["None", "Forward Checking", "Arc Consistency"],
            value="Arc Consistency",
            description="Filtering:",
            disabled=False,
            layout=widgets.Layout(margin="5px 0 5px 20px", align_self="center"),
        )

        self.speed_dropdown = Dropdown(
            options=["1x", "2x", "4x", "8x", "∞"],
            value="1x",
            description="Speed:",
            disabled=False,
            layout=widgets.Layout(margin="5px 0 5px 20px", align_self="center"),
        )

        # Button for resetting the solver configuration
        self.reset_button = Button(
            description="Reset",
            layout=widgets.Layout(width="135px", margin="0px 0 0px 25px"),
        )
        self.reset_button.on_click(self.on_reset_click)

        # Button for saving the solver configuration
        self.save_button = Button(
            description="Save",
            layout=widgets.Layout(width="135px", margin="0px 0 0px 7.5px"),
        )
        self.save_button.on_click(self.on_save_click)

        # Horizontal box to hold the buttons
        self.buttons_box = HBox(
            [self.reset_button, self.save_button],
            layout=widgets.Layout(margin="15px 0 5px 18px", align_self="center"),
        )

        # Creating a VBox to display the configuration UI along with buttons
        self.config_ui = VBox(
            [
                self.config_title,
                self.algorithm_dropdown,
                self.ordering_dropdown,
                self.filtering_dropdown,
                self.speed_dropdown,
                self.buttons_box,
            ],
            layout=widgets.Layout(margin="0px 0 0px -20px"),
        )
        return self.config_ui

    def on_reset_click(self, b):
        # Resetting dropdowns to their initial values
        self.speed_dropdown.value = self.speed_dropdown_reset
        self.algorithm_dropdown.value = self.algorithm_dropdown_reset
        self.ordering_dropdown.value = self.ordering_dropdown_reset
        self.filtering_dropdown.value = self.filtering_dropdown_reset

    def on_save_click(self, b):

        # Return to the main display
        self.on_button_click(
            b
        )  # This simulates clicking the AI button to return to main display

    def on_button_click(self, b):
        # If saving, return to main display, else show configuration
        if b.description == "Save":

            css = """
            <style>
            .button-style { 
                text-decoration: underline;
            }
            </style>
            """
            with self.output:
                clear_output(wait=True)
                display(HTML(css))
                display(
                    VBox(
                        [self.title, self.canvas, self.user_control],
                        layout=Layout(margin="-47.5px 0px 0 0px", width="875px"),
                    )
                )
        else:
            with self.output:
                clear_output(wait=True)
                display(self.config_ui)

    def on_ai_click(self, b):
        with self.output:
            self.ai_check.value = False
            self.algorithm_dropdown_reset = self.algorithm_dropdown.value
            self.ordering_dropdown_reset = self.ordering_dropdown.value
            self.filtering_dropdown_reset = self.filtering_dropdown.value
            self.speed_dropdown_reset = self.speed_dropdown.value
            clear_output(wait=True)
            display(self.config_ui)

    def speed_check(self):
        if self.speed_dropdown.value == "1x":
            return 1
        elif self.speed_dropdown.value == "2x":
            return 2
        elif self.speed_dropdown.value == "4x":
            return 4
        elif self.speed_dropdown.value == "8x":
            return 8
        else:
            return 0

    async def solve(self):

        self.board = [[0] * self.n for _ in range(self.n)]
        for r, c in self.positions:
            self.board[r][c] = 1

        self.update_threats_matrix()
        self.used_rows = set(r for (r, c) in self.positions)

        algorithm = self.algorithm_dropdown.value
        ordering = self.ordering_dropdown.value
        filtering = self.filtering_dropdown.value

        conflicts = self.count_conflicts()
        while conflicts != 0 and self.ai:
            row, col = self.find_most_conflict()
            # Backtracking
            self.board[row][col] = 0  # Remove the Queen
            # Backtrack threats
            self.backtrack_threats(self.threats, row, col)
            self.positions.remove((row, col))  # Remove Queen position

            used = True

            for y, x in self.positions:
                if y == row:
                    used = False
            if used:
                self.used_rows.remove(row)  # Remove row from used rows

            conflicts = self.count_conflicts()

            self.step_number += 1  # Update total step counter
            self.backtracking += 1  # Update backtracking step counter

            time = self.speed_check()
            if time != 0:
                self.steps.value = f"Total Steps: {self.step_number}"
                self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
                self.visualize_board()
                self.fig.canvas.draw()
                await asyncio.sleep(1 / time)

        # Call the appropriate solver method based on the configuration
        if algorithm == "Backtracking":
            if ordering == "MRV + LCV" and filtering == "Arc Consistency":
                solver = await self.solve_n_queens_util_mrv_lcv_ac()
            if ordering == "MRV + LCV" and filtering == "Forward Checking":
                solver = await self.solve_n_queens_util_mrv_lcv_fc()
            if ordering == "MRV + LCV" and filtering == "None":
                solver = await self.solve_n_queens_util_mrv_lcv()

            if ordering == "MRV" and filtering == "Arc Consistency":
                solver = await self.solve_n_queens_util_mrv_ac()
            if ordering == "MRV" and filtering == "Forward Checking":
                solver = await self.solve_n_queens_util_mrv_fc()
            if ordering == "MRV" and filtering == "None":
                solver = await self.solve_n_queens_util_mrv()

            if ordering == "LCV" and filtering == "Forward Checking":
                solver = await self.solve_n_queens_util_lcv_fc()
            if ordering == "LCV" and filtering == "Arc Consistency":
                solver = await self.solve_n_queens_util_lcv_ac()
            if ordering == "LCV" and filtering == "None":
                solver = await self.solve_n_queens_util_lcv()

            if ordering == "None" and filtering == "Arc Consistency":
                solver = await self.solve_n_queens_util_ac()
            if ordering == "None" and filtering == "Forward Checking":
                solver = await self.solve_n_queens_util_fc()
            if ordering == "None" and filtering == "None":
                solver = await self.solve_n_queens_util_backtracking()

        while not solver and self.ai:

            row, col = self.find_queen_to_remove()

            # Remove the queen that opens up most safe spots
            self.positions.remove((row, col))
            self.used_rows.remove(row)
            self.board[row][col] = 0
            self.backtrack_threats(self.threats, row, col)

            self.step_number += 1
            self.backtracking += 1

            time = self.speed_check()
            if time != 0:
                self.steps.value = f"Total Steps: {self.step_number}"
                self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
                self.visualize_board()
                self.fig.canvas.draw()
                await asyncio.sleep(1 / time)

            if algorithm == "Backtracking":
                if ordering == "MRV + LCV" and filtering == "Arc Consistency":
                    solver = await self.solve_n_queens_util_mrv_lcv_ac()
                if ordering == "MRV + LCV" and filtering == "Forward Checking":
                    solver = await self.solve_n_queens_util_mrv_lcv_fc()
                if ordering == "MRV + LCV" and filtering == "None":
                    solver = await self.solve_n_queens_util_mrv_lcv()

                if ordering == "MRV" and filtering == "Arc Consistency":
                    solver = await self.solve_n_queens_util_mrv_ac()
                if ordering == "MRV" and filtering == "Forward Checking":
                    solver = await self.solve_n_queens_util_mrv_fc()
                if ordering == "MRV" and filtering == "None":
                    solver = await self.solve_n_queens_util_mrv()

                if ordering == "LCV" and filtering == "Arc Consistency":
                    solver = await self.solve_n_queens_util_lcv_ac()
                if ordering == "LCV" and filtering == "Forward Checking":
                    solver = await self.solve_n_queens_util_lcv_fc()
                if ordering == "LCV" and filtering == "None":
                    solver = await self.solve_n_queens_util_lcv()

                if ordering == "None" and filtering == "Arc Consistency":
                    solver = await self.solve_n_queens_util_ac()
                if ordering == "None" and filtering == "Forward Checking":
                    solver = await self.solve_n_queens_util_fc()
                if ordering == "None" and filtering == "None":
                    solver = await self.solve_n_queens_util_backtracking()

        if self.ai and len(self.positions) == self.n and self.count_conflicts() == 0:

            self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
        self.visualize_board()
        self.fig.canvas.draw()

    ### Backtracking
    async def solve_n_queens_util_backtracking(self, row=0):
        if self.ai:
            if row >= self.n:
                return True

            if row in self.used_rows:
                if await self.solve_n_queens_util_fc(row + 1):
                    return True
            else:
                for col in range(self.n):
                    if self.is_safe(self.board, row, col):
                        if self.ai:
                            # Queen Placement
                            self.board[row][col] = 1  # Place the queen
                            self.update_threats(
                                self.threats, row, col
                            )  # Update threats
                            self.positions.add((row, col))  # Add Queen position
                            self.used_rows.add(row)  # Add row from used rows
                            self.step_number += 1  # Update total step counter
                            self.queen_placement += 1  # Update Queen placement counter

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)

                        if await self.solve_n_queens_util_backtracking(row + 1):
                            return True

                        if self.ai:
                            # Backtracking
                            self.board[row][col] = 0  # Remove the Queen
                            # Backtrack threats
                            self.backtrack_threats(self.threats, row, col)
                            self.positions.remove((row, col))  # Remove Queen position
                            self.used_rows.remove(row)  # Remove row from used rows
                            self.step_number += 1  # Update total step counter
                            self.backtracking += 1  # Update backtracking step counter

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()
                                await asyncio.sleep(1 / time)

        return False

    ### FC
    async def solve_n_queens_util_fc(self, row=0):
        if self.ai:
            if row >= self.n:
                return True

            if row in self.used_rows:
                if await self.solve_n_queens_util_fc(row + 1):
                    return True
            else:
                if self.forward_checking():

                    row_threats = self.threats[row]

                    safe_cols = [
                        index
                        for index, threats in enumerate(row_threats)
                        if threats == 0
                    ]

                    for col in safe_cols:

                        if self.ai:
                            # Queen Placement
                            self.board[row][col] = 1  # Place the queen
                            self.update_threats(
                                self.threats, row, col
                            )  # Update threats
                            self.positions.add((row, col))  # Add Queen position
                            self.used_rows.add(row)  # Add row from used rows
                            self.step_number += 1  # Update total step counter
                            self.queen_placement += 1  # Update Queen placement counter

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)

                        if await self.solve_n_queens_util_fc(row + 1):
                            return True

                        if self.ai:
                            # Backtracking
                            self.board[row][col] = 0  # Remove the Queen
                            # Backtrack threats
                            self.backtrack_threats(self.threats, row, col)
                            self.positions.remove((row, col))  # Remove Queen position
                            self.used_rows.remove(row)  # Remove row from used rows
                            self.step_number += 1  # Update total step counter
                            self.backtracking += 1  # Update backtracking step counter

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)
                else:
                    return False
        return False

    ### AC
    async def solve_n_queens_util_ac(self, row=0):
        if self.ai:
            if row >= self.n:
                return True

            if row in self.used_rows:
                if await self.solve_n_queens_util_ac(row + 1):
                    return True
            else:

                prune = self.arc_consistency(row)

                row_threats = self.threats[row]

                safe_cols = [
                    index for index, threats in enumerate(row_threats) if threats == 0
                ]

                for col in safe_cols:
                    if col not in prune:  # Check whether a column is pruned off

                        if self.ai:
                            # Queen Placement
                            self.board[row][col] = 1  # Place the queen
                            self.update_threats(
                                self.threats, row, col
                            )  # Update threats
                            self.positions.add((row, col))  # Add Queen position
                            self.used_rows.add(row)  # Add row from used rows
                            self.step_number += 1  # Update total step counter
                            self.queen_placement += 1  # Update Queen placement counter

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)

                        if await self.solve_n_queens_util_ac(row + 1):
                            return True

                        if self.ai:
                            # Backtracking
                            self.board[row][col] = 0  # Remove the Queen
                            # Backtrack threats
                            self.backtrack_threats(self.threats, row, col)
                            self.positions.remove((row, col))  # Remove Queen position
                            self.used_rows.remove(row)  # Remove row from used rows
                            self.step_number += 1  # Update total step counter
                            self.backtracking += 1  # Update backtracking step counter

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)
        return False

    ### LCV
    async def solve_n_queens_util_lcv(self, row=0):
        if self.ai:
            if row >= self.n:
                return True

            if row in self.used_rows:
                if await self.solve_n_queens_util_lcv(row + 1):
                    return True
            else:

                # Store a list of safe columns and number of remaining safe spots
                col_lcv = []
                for col in range(self.n):
                    if self.is_safe(self.board, row, col):
                        lcv = self.count_safe_spots_for_board(row, col)
                        col_lcv.append((col, lcv))

                # Sort the safe col in ascending order based on number of safe spots
                col_lcv.sort(key=lambda x: x[1])

                # Try Queen placement in each safe column (in LCV order) in this row
                for col, _ in col_lcv:
                    if self.ai:
                        self.board[row][col] = 1
                        self.update_threats(self.threats, row, col)
                        self.positions.add((row, col))
                        self.used_rows.add(row)

                        self.step_number += 1
                        self.queen_placement += 1

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)

                    if await self.solve_n_queens_util_lcv(row + 1):
                        return True

                    if self.ai and (row in self.used_rows):

                        self.board[row][col] = 0
                        self.backtrack_threats(self.threats, row, col)
                        self.positions.remove((row, col))
                        self.used_rows.remove(row)

                        self.step_number += 1
                        self.backtracking += 1

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)
        return False

    ### MRV
    async def solve_n_queens_util_mrv(self):
        if self.ai:

            # Base Case: all rows are occupied
            if len(self.used_rows) == self.n:
                return True

            # Find the target row with minimum remaining safe spots
            mrv_row = self.find_row_with_mrv()

            # Try Queen placement in each safe spot/column in this row
            for col in range(self.n):
                if self.is_safe(self.board, mrv_row, col):
                    if self.ai:
                        # Queen Placement
                        self.board[mrv_row][col] = 1  # Place the queen
                        self.update_threats(
                            self.threats, mrv_row, col
                        )  # Update threats
                        self.positions.add((mrv_row, col))  # Add Queen position
                        self.used_rows.add(mrv_row)  # Add row from used rows
                        self.step_number += 1  # Update total step counter
                        self.queen_placement += 1  # Update Queen placement counter

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)

                    # Recursively call function onto next row
                    if await self.solve_n_queens_util_mrv():
                        return True

                    if self.ai:
                        # Backtracking
                        self.board[mrv_row][col] = 0  # Remove the Queen
                        self.backtrack_threats(
                            self.threats, mrv_row, col
                        )  # Backtrack threats
                        self.positions.remove((mrv_row, col))  # Remove Queen position
                        self.used_rows.remove(mrv_row)  # Remove row from used rows
                        self.step_number += 1  # Update total step counter
                        self.backtracking += 1  # Update backtracking step counter

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)
        return False

    ### MRV + LCV
    async def solve_n_queens_util_mrv_lcv(self):
        if self.ai:

            if len(self.used_rows) == self.n:
                return True

            mrv_row = self.find_row_with_mrv()
            col_lcv = []
            for col in range(self.n):
                if self.is_safe(self.board, mrv_row, col):
                    lcv = self.count_safe_spots_for_board(mrv_row, col)
                    col_lcv.append((col, lcv))
            col_lcv.sort(key=lambda x: x[1])

            for col, _ in col_lcv:
                if self.ai:
                    self.board[mrv_row][col] = 1
                    self.update_threats(self.threats, mrv_row, col)
                    self.positions.add((mrv_row, col))
                    self.used_rows.add(mrv_row)

                    self.step_number += 1
                    self.queen_placement += 1

                    time = self.speed_check()
                    if time != 0:
                        self.steps.value = f"Total Steps: {self.step_number}"
                        self.placements.value = (
                            f"Total Queen Placements: {self.queen_placement}"
                        )
                        self.backtracks.value = (
                            f"Total Backtracking Steps: {self.backtracking}"
                        )
                        self.visualize_board()
                        self.fig.canvas.draw()

                        await asyncio.sleep(1 / time)

                if await self.solve_n_queens_util_mrv_lcv():
                    return True

                if self.ai:
                    self.board[mrv_row][col] = 0
                    self.backtrack_threats(self.threats, mrv_row, col)
                    self.positions.remove((mrv_row, col))
                    self.used_rows.remove(mrv_row)

                    self.step_number += 1
                    self.backtracking += 1

                    time = self.speed_check()
                    if time != 0:
                        self.steps.value = f"Total Steps: {self.step_number}"
                        self.placements.value = (
                            f"Total Queen Placements: {self.queen_placement}"
                        )
                        self.backtracks.value = (
                            f"Total Backtracking Steps: {self.backtracking}"
                        )
                        self.visualize_board()
                        self.fig.canvas.draw()

                        await asyncio.sleep(1 / time)

        return False

    ### LCV + AC
    async def solve_n_queens_util_lcv_ac(self, row=0):
        if self.ai:
            if row >= self.n:
                return True

            if row in self.used_rows:
                if await self.solve_n_queens_util_lcv_fc(row + 1):
                    return True
            else:

                # Find the list of safe columns to prune off
                prune = self.arc_consistency(row)

                # Store a list of safe columns and number of remaining safe spots
                col_lcv = []
                for col in range(self.n):
                    if self.is_safe(self.board, row, col):
                        lcv = self.count_safe_spots_for_board(row, col)
                        col_lcv.append((col, lcv))

                # Sort the safe col in ascending order based on number of safe spots
                col_lcv.sort(key=lambda x: x[1])

                # Try Queen placement in each safe column (in LCV order) in this row
                for col, _ in col_lcv:
                    if col not in prune:  # Check whether a column is pruned off
                        if self.ai:
                            self.board[row][col] = 1
                            self.update_threats(self.threats, row, col)
                            self.positions.add((row, col))
                            self.used_rows.add(row)

                            self.step_number += 1
                            self.queen_placement += 1

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)

                        if await self.solve_n_queens_util_lcv_ac(row + 1):
                            return True

                        if self.ai and (row in self.used_rows):

                            self.board[row][col] = 0
                            self.backtrack_threats(self.threats, row, col)
                            self.positions.remove((row, col))
                            self.used_rows.remove(row)

                            self.step_number += 1
                            self.backtracking += 1

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)

        return False

    ### LCV + FC
    async def solve_n_queens_util_lcv_fc(self, row=0):
        if self.ai:
            if row >= self.n:
                return True

            if row in self.used_rows:
                if await self.solve_n_queens_util_lcv_fc(row + 1):
                    return True
            else:
                # Filtering: Forward Checking
                if self.forward_checking():

                    col_lcv = []
                    for col in range(self.n):
                        if self.is_safe(self.board, row, col):
                            lcv = self.count_safe_spots_for_board(row, col)
                            col_lcv.append((col, lcv))
                    col_lcv.sort(key=lambda x: x[1])

                    for col, _ in col_lcv:
                        if self.ai:
                            self.board[row][col] = 1
                            self.update_threats(self.threats, row, col)
                            self.positions.add((row, col))
                            self.used_rows.add(row)

                            self.step_number += 1
                            self.queen_placement += 1

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)

                        if await self.solve_n_queens_util_lcv_fc(row + 1):
                            return True

                        if self.ai and (row in self.used_rows):

                            self.board[row][col] = 0
                            self.backtrack_threats(self.threats, row, col)
                            self.positions.remove((row, col))
                            self.used_rows.remove(row)

                            self.step_number += 1
                            self.backtracking += 1

                            time = self.speed_check()
                            if time != 0:
                                self.steps.value = f"Total Steps: {self.step_number}"
                                self.placements.value = (
                                    f"Total Queen Placements: {self.queen_placement}"
                                )
                                self.backtracks.value = (
                                    f"Total Backtracking Steps: {self.backtracking}"
                                )
                                self.visualize_board()
                                self.fig.canvas.draw()

                                await asyncio.sleep(1 / time)
                else:
                    return False

        return False

    ### MRV + LCV + FC
    async def solve_n_queens_util_mrv_lcv_fc(self):
        if self.ai:
            if len(self.used_rows) == self.n:
                return True

            # Filtering: Forward Checking
            if self.forward_checking():
                # Find the target row with minimum remaining safe spots
                mrv_row = self.find_row_with_mrv()

                col_lcv = []
                for col in range(self.n):
                    if self.is_safe(self.board, mrv_row, col):
                        lcv = self.count_safe_spots_for_board(mrv_row, col)
                        col_lcv.append((col, lcv))
                col_lcv.sort(key=lambda x: x[1])

                for col, _ in col_lcv:
                    if self.ai:
                        self.board[mrv_row][col] = 1
                        self.update_threats(self.threats, mrv_row, col)
                        self.positions.add((mrv_row, col))
                        self.used_rows.add(mrv_row)

                        self.step_number += 1
                        self.queen_placement += 1

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)

                    if await self.solve_n_queens_util_mrv_lcv_fc():
                        return True
                    if self.ai:

                        self.board[mrv_row][col] = 0
                        self.backtrack_threats(self.threats, mrv_row, col)
                        self.positions.remove((mrv_row, col))
                        self.used_rows.remove(mrv_row)

                        self.step_number += 1
                        self.backtracking += 1

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)
            else:
                return False

        return False

    ### MRV + FC
    async def solve_n_queens_util_mrv_fc(self):
        if self.ai:
            if len(self.used_rows) == self.n:
                return True

            # Filtering: Forward Checking
            if self.forward_checking():
                # Find the target row with minimum remaining safe spots
                mrv_row = self.find_row_with_mrv()

                row_threats = self.threats[mrv_row]  # Threats value for current row
                # Extract index of safe columns based on row threats list
                safe_cols = [
                    index for index, threats in enumerate(row_threats) if threats == 0
                ]

                # Try Queen placement in each safe column in this row
                for col in safe_cols:
                    if self.ai:
                        # Queen Placement
                        self.board[mrv_row][col] = 1  # Place the queen
                        self.update_threats(
                            self.threats, mrv_row, col
                        )  # Update threats
                        self.positions.add((mrv_row, col))  # Add Queen position
                        self.used_rows.add(mrv_row)  # Add row from used rows
                        self.step_number += 1  # Update total step counter
                        self.queen_placement += 1  # Update Queen placement counter

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)

                    # Recursively call function onto next row
                    if await self.solve_n_queens_util_mrv_fc():
                        return True

                    if self.ai:
                        # Backtracking
                        self.board[mrv_row][col] = 0  # Remove the Queen
                        self.backtrack_threats(
                            self.threats, mrv_row, col
                        )  # Backtrack threats
                        self.positions.remove((mrv_row, col))  # Remove Queen position
                        self.used_rows.remove(mrv_row)  # Remove row from used rows
                        self.step_number += 1  # Update total step counter
                        self.backtracking += 1  # Update backtracking step counter

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)

            else:
                return False

        return False

    ### MRV + AC

    async def solve_n_queens_util_mrv_ac(self):
        if self.ai:
            if len(self.used_rows) == self.n:
                return True

            mrv_row = self.find_row_with_mrv()

            prune = self.arc_consistency(mrv_row)

            row_threats = self.threats[mrv_row]

            safe_cols = [
                index for index, threats in enumerate(row_threats) if threats == 0
            ]

            for col in safe_cols:
                if col not in prune:  # Check whether a column is pruned off

                    if self.ai:
                        # Queen Placement
                        self.board[mrv_row][col] = 1  # Place the queen
                        self.update_threats(
                            self.threats, mrv_row, col
                        )  # Update threats
                        self.positions.add((mrv_row, col))  # Add Queen position
                        self.used_rows.add(mrv_row)  # Add row from used rows
                        self.step_number += 1  # Update total step counter
                        self.queen_placement += 1  # Update Queen placement counter

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)

                    if await self.solve_n_queens_util_mrv_ac():
                        return True

                    if self.ai:
                        # Backtracking
                        self.board[mrv_row][col] = 0  # Remove the Queen
                        # Backtrack threats
                        self.backtrack_threats(self.threats, mrv_row, col)
                        self.positions.remove((mrv_row, col))  # Remove Queen position
                        self.used_rows.remove(mrv_row)  # Remove row from used rows
                        self.step_number += 1  # Update total step counter
                        self.backtracking += 1  # Update backtracking step counter

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)

        return False

    ### MRV + LCV + AC

    async def solve_n_queens_util_mrv_lcv_ac(self):
        if self.ai:
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
                    if self.ai:
                        self.board[mrv_row][col] = 1
                        self.update_threats(self.threats, mrv_row, col)
                        self.positions.add((mrv_row, col))
                        self.used_rows.add(mrv_row)

                        self.step_number += 1
                        self.queen_placement += 1

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)

                    if await self.solve_n_queens_util_mrv_lcv_ac():
                        return True

                    if self.ai:
                        self.board[mrv_row][col] = 0
                        self.backtrack_threats(self.threats, mrv_row, col)
                        self.positions.remove((mrv_row, col))
                        self.used_rows.remove(mrv_row)

                        self.step_number += 1
                        self.backtracking += 1

                        time = self.speed_check()
                        if time != 0:
                            self.steps.value = f"Total Steps: {self.step_number}"
                            self.placements.value = (
                                f"Total Queen Placements: {self.queen_placement}"
                            )
                            self.backtracks.value = (
                                f"Total Backtracking Steps: {self.backtracking}"
                            )
                            self.visualize_board()
                            self.fig.canvas.draw()

                            await asyncio.sleep(1 / time)
        return False

    ### Solver Helper Functions ###
    def forward_checking(self):
        safe = False  # Boolean flag to return (True: Continue; False: Backtrack)
        for i in range(self.n):
            if i not in self.used_rows:
                safe = False
                for j in range(self.n):
                    if self.threats[i][j] == 0:
                        safe = True
                        break
                if not safe:
                    return False
        return safe

    def update_threats_matrix(self):
        self.threats = [[0] * self.n for _ in range(self.n)]
        for r, c in self.positions:
            self.update_threats(self.threats, r, c)

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

    def look_ahead(self, threats, row):
        safe = False
        for j in range(self.n):
            if threats[row][j] == 0:
                safe = True
                break
        return safe

    def find_queen_to_remove(self):
        max_safe = -1
        row_r = -1
        col_r = -1
        for row, col in self.positions:
            safe_spots = self.count_safe_spots_for_board_remove(row, col)
            if safe_spots > max_safe:
                max_safe = safe_spots
                row_r = row
                col_r = col
        return row_r, col_r

    def count_safe_spots_for_board_remove(self, row, col):
        board_copy = [r[:] for r in self.board]
        board_copy[row][col] = 0
        safe_spots = 0
        for r in range(self.n):
            for c in range(self.n):
                if self.is_safe(board_copy, r, c):
                    safe_spots += 1
        return safe_spots

    def count_safe_spots_for_board(self, row, col):
        board_copy = [r[:] for r in self.board]
        board_copy[row][col] = 1
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

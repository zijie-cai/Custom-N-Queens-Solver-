import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from ipywidgets import widgets, Button, HBox, VBox, Layout, Output
from IPython.display import clear_output, display
import asyncio
import random


class N_Queens_Game:
    def __init__(self):
        self.start = True
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
        self.title = widgets.Label(
            value="N-Queens Playground",
            style={"font_weight": "bold", "font_size": "20px"},
            layout=widgets.Layout(margin="10px 0 0px 0px"),
        )
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
        self.visualize_board()

    def setup(self):
        self.reset = Button(description="New", layout=Layout(width="150px"))
        self.reset.on_click(self.new_reset)

        self.hint_check = widgets.Checkbox(value=False, indent=False)
        hint_label = widgets.Label("Hint", layout=Layout(margin="0px 0 0 -280px"))
        self.hint_widget = HBox(
            [self.hint_check, hint_label],
            layout=Layout(width="100%", margin="2.5px 0 0 20px", overflow="hidden"),
        )

        self.ai_check = widgets.Checkbox(value=False, indent=False)
        ai_label = widgets.Label("AI", layout=Layout(margin="0px 0 0 -280px"))
        self.ai_widget = HBox(
            [self.ai_check, ai_label],
            layout=Layout(width="100%", margin="2.5px 0 0 -75px", overflow="hidden"),
        )

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
        user_control = VBox(
            [self.size, button_row, stats_box],
            layout=Layout(margin="0 0 0 55px", overflow="hidden"),
        )
        title = VBox([self.title], layout=Layout(margin="35px 0 5px 75px"))

        with self.output:
            display(
                VBox(
                    [title, self.fig.canvas, user_control],
                    layout=Layout(margin="-47.5px 0px 0 0px"),
                )
            )

        display(self.output)

    def observe_hint(self, change):
        self.hint = change["new"]
        self.visualize_board()

    def observe_ai(self, change):
        self.ai = change["new"]
        if self.ai:
            asyncio.create_task(self.start_ai_solver())

    def new_reset(self, change=None):
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

        for y, x in self.positions:
            img = OffsetImage(queen_img, zoom=zoom_factor)
            ab = AnnotationBbox(
                img, (x + 0.5, y + 0.5), frameon=False, boxcoords="data", pad=0
            )
            self.ax.add_artist(ab)

        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, self.n)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        title_font = {"fontsize": 10}
        self.ax.set_title(
            "AI-Queens" if self.start else f"{self.n}-Queens", fontdict=title_font
        )
        self.ax.invert_yaxis()
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        if self.hint:
            for y in range(self.n):
                for x in range(self.n):
                    if (y, x) not in self.positions:
                        threat = self.compute_threats(y, x)
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

    def compute_threats(self, row, col):
        threats = 0
        for y, x in self.positions:
            if y == row or x == col or abs(y - row) == abs(x - col):
                threats += 1
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

    def onclick(self, event):
        if event.inaxes and event.xdata is not None and event.ydata is not None:
            row, col = int(event.ydata), int(event.xdata)
            if (row, col) not in self.positions and self.compute_threats(row, col) == 0:
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

            if self.start and self.is_board_safe():
                self.start = False

            if len(self.positions) == self.n:
                self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
            else:
                self.ai_check.value = False
                self.solution.value = ""

    async def start_ai_solver(self):
        await self.make_board_safe()
        if self.start and self.is_board_safe():
            self.start = False
        await self.solve()
        self.steps.value = f"Total Steps: {self.step_number}"
        self.placements.value = f"Total Queen Placements: {self.queen_placement}"
        self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
        if len(self.positions) == self.n:
            self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
        else:
            self.solution.value = ""

    async def make_board_safe(self):
        while not self.is_board_safe() and self.positions and self.ai:
            row, col = random.choice(list(self.positions))
            self.positions.remove((row, col))
            self.update_threats_matrix()
            self.step_number += 1
            self.backtracking += 1
            self.steps.value = f"Total Steps: {self.step_number}"
            self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
            self.visualize_board()
            self.fig.canvas.draw()
            await asyncio.sleep(0.25)  # Use asyncio.sleep for non-blocking delay

    async def solve(self):
        self.board = [[0] * self.n for _ in range(self.n)]
        for r, c in self.positions:
            self.board[r][c] = 1

        self.update_threats_matrix()
        self.used_rows = set(r for (r, c) in self.positions)

        # Backtracking Solver
        while not await self.solve_n_queens_util() and self.ai:

            row, col = self.find_queen_to_remove()

            # Remove the queen that opens up most safe spots
            self.positions.remove((row, col))
            self.used_rows.remove(row)
            self.board[row][col] = 0
            self.backtrack_threats(self.threats, row, col)

            self.step_number += 1
            self.backtracking += 1
            self.steps.value = f"Total Steps: {self.step_number}"
            self.backtracks.value = f"Total Backtracking Steps: {self.backtracking}"
            self.visualize_board()
            self.fig.canvas.draw()
            await asyncio.sleep(0.25)

        if self.ai and len(self.positions) == self.n:
            self.solution.value = '<span style="color:#769656; font-weight:bold; font-size:15px;">Solution Found!</span>'
        self.visualize_board()

    async def solve_n_queens_util(self):
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
                        self.steps.value = f"Total Steps: {self.step_number}"
                        self.placements.value = (
                            f"Total Queen Placements: {self.queen_placement}"
                        )
                        self.backtracks.value = (
                            f"Total Backtracking Steps: {self.backtracking}"
                        )
                        self.visualize_board()
                        self.fig.canvas.draw()
                        await asyncio.sleep(0.25)
                    if await self.solve_n_queens_util():
                        return True
                    if self.ai:
                        self.board[mrv_row][col] = 0
                        self.backtrack_threats(self.threats, mrv_row, col)
                        self.positions.remove((mrv_row, col))
                        self.used_rows.remove(mrv_row)
                        self.step_number += 1
                        self.backtracking += 1
                        self.steps.value = f"Total Steps: {self.step_number}"
                        self.placements.value = (
                            f"Total Queen Placements: {self.queen_placement}"
                        )
                        self.backtracks.value = (
                            f"Total Backtracking Steps: {self.backtracking}"
                        )
                        self.visualize_board()
                        self.fig.canvas.draw()
                        await asyncio.sleep(0.25)
        return False

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

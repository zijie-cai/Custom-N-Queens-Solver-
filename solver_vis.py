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
    img_output_area = widgets.Output(layout=widgets.Layout(margin="0 0 0 -50px"))

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
                value=0, min=0, max=max_img, description="Progress:"
            )

            # Progress label for status of visualization generation
            progress_label = widgets.Label("0% Complete")

            # Combine progress bar and label horizontally in list order
            progress_box = widgets.HBox(
                [progress_bar, progress_label],
                layout=widgets.Layout(margin="0 0 0 40px"),
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
                layout=widgets.Layout(overflow="hidden", margin="20px 0 0 50px"),
            )

            # Display for right output area
            display(right_box)

            # Initialize first image step for display
            solver_vis.display_figure(0)

    # Link solve button to trigger function events (run solver) when clicked
    solve_button.on_click(click_solve_button)

    # Combine both left and right output area horizontally and display
    layout_box = widgets.HBox([left_box, right_box])
    display(layout_box)

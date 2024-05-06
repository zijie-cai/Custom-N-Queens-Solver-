# ♕ Custom N-Queens Solver ♕
This repository showcases an intuitive visualization tool for understanding the effects of Algorithms, Ordering Heuristics, and Filtering Techniques while solving N-Queens as a Constraint Satisfaction Problem (CSP).

## Overview 
The N queens problem involves placing N queens on an NxN chessboard in such a way that no two queens threaten each other. It's a classic example of a constraint satisfaction problem (CSP), where the objective is to find a solution that satisfies all constraints.

The N-Queens problem involves placing N number of Queens on a size N x N chessboard in a way such that no two Queens threaten each other. The approach is to formulate this as a CSP problem: 

1. **Variables:** 
    - Rows on the board; the algorithm finds a solution by traversing through the board row by row (default).

2. **Domain:**  
   - Columns for each row on the board; the algorithm finds a solution by whether a column spot is safe/unthreatened. 

3. **Constraints:**
   - No two Queens can be in the same row. 
   - No two Queens can be in the same column. 
   - No two Queens can be on the same diagonal (both directions). 

## Installation and Setup 
- Create and activate a virtual environment (to your liking):
- Install required libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```
## How to Use 
Simply clone or download the repository and follow the `vis_tool.ipynb` Jupyter Notebook.

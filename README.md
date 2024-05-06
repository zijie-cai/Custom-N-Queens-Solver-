# ♕ Custom N-Queens Solver ♕
This repository showcases an intuitive visualization tool for understanding the effects of Algorithms, Ordering Heuristics, and Filtering Techniques while solving N-Queens as a Constraint Satisfaction Problem (CSP).

## Overview 
The N-Queens problem involves placing N number of Queens on a size N x N chessboard in a way such that no two Queens threaten each other. The approach is to formulate this as a CSP problem, where the goal is to find a satisfied solution without violating any constraints. 

### CSP Formulation

**Variables:** 
   - Rows on the board; the algorithm finds a solution by traversing through the board row by row (default).

**Domain:**  
   - Columns for each row on the board; the algorithm finds a solution by whether a column spot is safe/unthreatened. 

**Constraints:**
   - No two Queens can be in the same row. 
   - No two Queens can be in the same column. 
   - No two Queens can be on the same diagonal (both directions).
   - Exactly N Queens on the board when a solution is found.

### Algorithms
- **Backtracking Search:**  

- **Ordering Heuristics:**
  - **Minimum Remaining Values (MRV/MCV):**  
  - **Least Constraining Value (LCV):**  

- **Filtering Techniques:**
  - **Arc Consistency:**  
  
  - **Forward Checking:**

- **Combined Strategies:**  


## Installation and Setup 
- Create and activate a virtual environment (to your liking):
- Install required libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```
## How to Use 
Simply clone or download the repository and follow the `vis_tool.ipynb` Jupyter Notebook.

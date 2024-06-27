# ♕ N-Queens Playground + AI CSP Solver ♕
This repository showcases an intuitive visualization tool for understanding the various effects of Algorithms, Ordering Heuristics, and Filtering Techniques while solving N-Queens as a Constraint Satisfaction Problem (CSP).

<p align="center">
  <img src="demo1.png" width="400"/>
  <img src="demo2.png" width="400"/>
</p>

## Quick Access
You can access the N-Queens Playground hosted on Binder without the need to install anything locally.

**Click the Link:** [N-Queens-Playground](https://mybinder.org/v2/gh/zijie-cai/N-Queens-Playground/HEAD?urlpath=%2Fvoila%2Frender%2Fn_queens_playground.ipynb)

## Overview 
The N-Queens problem involves placing N number of Queens on a size N x N chessboard in a way such that no two Queens can threaten each other. The approach is to formulate N-Queens as a CSP problem, where the objective is to find a solution of Queen placements on the board that satisfies all pre-defined constraints.

### CSP Formulation
- **Variables:** 
   - Rows on the board
- **Domain:**  
   - Columns for each row on the board
- **Constraints:**
   - No two Queens can share the same row. 
   - No two Queens can share the same column. 
   - No two Queens can share the same diagonal (both directions).
   - Exactly N Queens on the board when a solution is found.
     
### Solve Methods
- **Algorithms**
  - Backtracking Search  
- **Ordering Heuristics:**
  - Minimum Remaining Values / Most Constraining Variable (MRV/MCV)
  - Least Constraining Value (LCV)
- **Filtering Techniques:**
  - Forward Checking
  - Arc Consistency  
- **Combined Strategies**  
  - MRV + LCV
  - Ordering + Filtering

## Use Locally
- Clone the repository
- Create and activate a virtual Python environment (to your liking):
- Install required libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```
    
## Potential Improvements
- Enhance the N-Queens Game by adding more constraints
- Add support for more solver algorithms

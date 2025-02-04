***A Search for 8‐Puzzle (with Diagonal Moves)***

**Project Overview**

This project implements the A* (A‐star) search algorithm to solve a 3×3 sliding puzzle (commonly known as the 8‐puzzle). In this particular variant, diagonal blank moves are allowed, each with a cost of 1.4. Orthogonal moves (up/down/left/right) each have a cost of 1.

The code prints a partial search tree: for each expanded puzzle state, it shows:

1) The expansion order (which step in the search the node was explored).
2) The puzzle layout.
3) The costs (g,h,f).
4) The child states discovered from that node.

By default, the code limits how many expansions are performed for demonstration purposes, so you can see the step‐by‐step search without excessive output.

***File Contents***

test.py contains the entire implementation including:

1) A representation of the puzzle and how to print it.
2) An octile distance heuristic function.
3) A routine to generate neighboring states (including diagonal moves).
4) The A* search function itself, with a limit on how many states to expand.
5) A print routine that outputs the search expansions in a human‐readable format.

***How to Run***

1) Install Python (version 3.x) if you haven’t already.
2) Clone or Download this project folder to your local machine.
3) Open a terminal (or command prompt) and navigate (cd) into the folder containing eight_puzzle_astar.py.

Run the script:

python test.py

On some systems, you might use:

python3 test.py


View the output in your terminal window. You will see a series of expansions printed, including their expansion number, the puzzle layout, and costs (g,h,f).

***Usage & Customization***

**Change max_expansions:**

If you want to see more of the search tree or reach the goal more reliably, open eight_puzzle_astar.py and find:

expansions_dict, found = a_star_search(start_state, goal_state, max_expansions=15)

Increase max_expansions to a higher value (e.g., 1000).

***Modify Start/Goal States:***

You can change:

start_state = (0,1,3, 8,2,6, 7,5,4)
goal_state  = (1,2,3, 8,0,4, 7,6,5)

to other puzzle configurations as desired. 

**Remember:**

- The blank is represented by 0.
- The 3×3 puzzle is represented in row‐major order as a 9‐tuple.

***Reconstructing the Path to Goal (optional):***
If you reach the goal within the expansion limit, you can modify the code to backtrack from the goal node to the start node using the stored parent references. This lets you see the exact sequence of moves.


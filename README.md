This is a small personal project where I use A* search to solve a 3×3 sliding puzzle (the classic 8‐puzzle) but with a twist: the blank can move diagonally (cost = 1.4) as well as orthogonally (cost = 1). The code is just one Python file, and here’s how you can run and tweak it.

You need Python 3 installed. Put the file (for example, test.py) in a folder. Open a terminal, go to that folder, and run:

```python

python test.py

```

Inside the code, the start and goal states are tuples of length 9 in row‐major order, with 0 representing the blank.

By default:

```python
start_state = (0,1,3, 8,2,6, 7,5,4)
goal_state  = (1,2,3, 8,0,4, 7,6,5)
```

You can change these to any other valid 3×3 arrangement. The code prints a partial search tree: each state’s expansion order, puzzle layout, and costs (g, h, and f). There’s a parameter max_expansions that limits how many nodes the algorithm will expand before stopping, just so the output doesn’t get too big:

```python
expansions_dict, found = a_star_search(start_state, goal_state, max_expansions=15)
```

You can increase max_expansions if you want to see more steps or fully solve the puzzle. If the goal is reached, the code will say so; if not, it means the limit stopped the search early. If you need the actual path of moves, you can modify the script to backtrack from the goal to the start using the stored parent references.

That’s it! When you run it, you’ll see lines like:

```python
Expansion #1
State: (g=0.00, h=5.40, f=5.40)
_  1  3
8  2  6
7  5  4

Children:
  -> g=1.00, h=4.40, f=5.40 (not expanded yet)
  -> ...
```

This shows how the algorithm checks different puzzle states, their costs, and so on. Enjoy exploring the 8‐puzzle with diagonal moves!

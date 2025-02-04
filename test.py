import math
import heapq

###############################################################################
# A small utility to pretty-print the 3x3 puzzle state
###############################################################################
def print_puzzle(state_tuple):
    """
    state_tuple is a length-9 tuple representing row-major 3x3 puzzle.
    Example: (0,1,3,8,2,6,7,5,4) means:
       Row0: [0, 1, 3]
       Row1: [8, 2, 6]
       Row2: [7, 5, 4]
    where '0' denotes the blank.
    """
    for row in range(3):
        row_vals = state_tuple[3*row : 3*row+3]
        print("  ".join("_" if v==0 else str(v) for v in row_vals))
    print()

###############################################################################
# Heuristic Function: "Octile Distance" for each tile
#    - If diagonal moves are allowed, we measure how many diagonal steps
#      + straight steps it takes to get each tile from current to goal.
###############################################################################
def octile_distance_heuristic(state, goal):
    """
    Returns the sum of octile distances for all tiles (ignoring the blank).
    """
    dist_sum = 0.0
    for tile in range(1, 9):  # tiles 1..8
        # current index of tile in 'state'
        curr_index = state.index(tile)
        curr_r, curr_c = divmod(curr_index, 3)
        
        # goal index of tile in 'goal'
        goal_index = goal.index(tile)
        goal_r, goal_c = divmod(goal_index, 3)
        
        # horizontal/vertical differences
        dx = abs(curr_r - goal_r)
        dy = abs(curr_c - goal_c)
        
        # octile distance: diagonal steps + straight steps
        diagonal = min(dx, dy)
        straight = max(dx, dy) - diagonal
        dist_sum += 1.4*diagonal + 1.0*straight
    return dist_sum

###############################################################################
# Get neighbors (child states) of a given state by sliding the blank (0).
# We allow 8 directions: up, down, left, right, and 4 diagonals if valid.
###############################################################################
def get_neighbors(state):
    """
    Returns a list of (child_state, move_cost) for each valid blank move.
    """
    neighbors = []
    
    # Locate blank
    blank_index = state.index(0)
    r, c = divmod(blank_index, 3)
    
    # All possible moves for the blank, with (dr, dc) indicating row/col shifts
    moves = [
        (-1, 0, 1.0),  # Up
        (1, 0, 1.0),   # Down
        (0, -1, 1.0),  # Left
        (0, 1, 1.0),   # Right
        (-1, -1, 1.4), # Diagonal up-left
        (-1, 1, 1.4),  # Diagonal up-right
        (1, -1, 1.4),  # Diagonal down-left
        (1, 1, 1.4),   # Diagonal down-right
    ]
    
    for (dr, dc, cost) in moves:
        rr = r + dr
        cc = c + dc
        if 0 <= rr < 3 and 0 <= cc < 3:
            # valid position to swap with blank
            new_index = rr*3 + cc
            # swap blank with that tile
            new_state = list(state)
            new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
            neighbors.append((tuple(new_state), cost))
    
    return neighbors

###############################################################################
# A* Search
###############################################################################
def a_star_search(start, goal, max_expansions=15):
    """
    Perform A* search from start to goal. 
    max_expansions limits how many nodes we expand (for demo visualization).
    
    Returns:
       expansions: dict keyed by state, storing:
          {
             "parent": the state from which this was expanded,
             "g": cost so far,
             "h": heuristic,
             "f": g + h,
             "expansion_order": int expansion count,
             "children": list of child states discovered from this node
          }
       reached_goal: the goal state (if found) or None
    """
    
    # Priority queue for the open list; stores (f, count, state)
    # 'count' is a tie-breaker so Python doesn't complain about ties
    open_list = []
    expansions = {}  # Map: state -> info
    
    # Initialize
    g_start = 0.0
    h_start = octile_distance_heuristic(start, goal)
    f_start = g_start + h_start
    
    expansions[start] = {
        "parent": None,
        "g": g_start,
        "h": h_start,
        "f": f_start,
        "expansion_order": None,  # to be assigned once popped
        "children": []
    }
    
    count = 0  # tie-breaker for the priority queue
    heapq.heappush(open_list, (f_start, count, start))
    
    # A set for visited states
    closed_set = set()
    expansion_counter = 0
    
    # Begin the search
    while open_list and expansion_counter < max_expansions:
        _, _, current = heapq.heappop(open_list)
        
        if current in closed_set:
            continue
        
        # Mark expansion
        expansion_counter += 1
        expansions[current]["expansion_order"] = expansion_counter
        
        # Check for goal
        if current == goal:
            return expansions, current
        
        # Add current to closed set
        closed_set.add(current)
        
        # Expand neighbors
        for (nbr_state, move_cost) in get_neighbors(current):
            if nbr_state in closed_set:
                continue
            
            # Cost to neighbor
            g_new = expansions[current]["g"] + move_cost
            h_new = octile_distance_heuristic(nbr_state, goal)
            f_new = g_new + h_new
            
            # If this neighbor not seen yet or we found a cheaper path:
            if nbr_state not in expansions or f_new < expansions[nbr_state]["f"]:
                expansions[nbr_state] = {
                    "parent": current,
                    "g": g_new,
                    "h": h_new,
                    "f": f_new,
                    "expansion_order": None,  # will set when popped
                    "children": []
                }
                expansions[current]["children"].append(nbr_state)
                
                count += 1
                heapq.heappush(open_list, (f_new, count, nbr_state))
    
    # If we exit the loop without finding goal (or expansions exhausted):
    return expansions, None

###############################################################################
# Utility to print a small search "tree" in the order of expansions
###############################################################################
def print_search_expansions(expansions, start):
    """
    Prints each expanded state in ascending order of expansion_order.
    Shows g, h, f, and the puzzle layout.
    Also shows that node's children.
    """
    # Sort states by their expansion order (ignoring unexpanded which are None)
    expanded_states = [s for s in expansions if expansions[s]["expansion_order"] is not None]
    expanded_states.sort(key=lambda s: expansions[s]["expansion_order"])
    
    for s in expanded_states:
        order = expansions[s]["expansion_order"]
        g_val = expansions[s]["g"]
        h_val = expansions[s]["h"]
        f_val = expansions[s]["f"]
        
        print(f"==========================")
        print(f"Expansion #{order}")
        print(f"State: (expansion_order={order}, g={g_val:.2f}, h={h_val:.2f}, f={f_val:.2f})")
        print_puzzle(s)
        
        # Print children (just list them by their puzzle arrangement)
        child_list = expansions[s]["children"]
        if child_list:
            print("  Children:")
            for c in child_list:
                # If it has not been assigned an expansion_order yet, it wasn't expanded
                ch_order = expansions[c]["expansion_order"]
                if ch_order is None:
                    ch_str = "(not expanded yet)"
                else:
                    ch_str = f"(expanded #{ch_order})"
                print(f"    -> g={expansions[c]['g']:.2f}, "
                      f"h={expansions[c]['h']:.2f}, "
                      f"f={expansions[c]['f']:.2f} {ch_str}")
            print()
        else:
            print("  Children: None\n")

###############################################################################
# MAIN DEMO
###############################################################################
if __name__ == "__main__":
    
    # Example Start and Goal states:
    # Start  (as shown in the question figure):
    #   0 1 3
    #   8 2 6
    #   7 5 4
    # Goal:
    #   1 2 3
    #   8 0 4
    #   7 6 5
    start_state = (0,1,3, 8,2,6, 7,5,4)
    goal_state  = (1,2,3, 8,0,4, 7,6,5)
    
    # Run A* with a small expansion limit (for visualization)
    expansions_dict, found = a_star_search(start_state, goal_state, max_expansions=15)
    
    # Print out the expansions in order
    print("A* SEARCH EXPANSION TRACE (partial)\n")
    print_search_expansions(expansions_dict, start_state)
    
    # If goal was reached within our expansion limit, show success
    if found is not None:
        print("Goal was reached within the expansion limit!\n")
        # You could reconstruct the path here if desired.
    else:
        print("Goal NOT reached within the expansion limit.\n")

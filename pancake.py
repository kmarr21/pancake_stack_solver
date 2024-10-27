import random
import fibheap

# wrapper class: ensure correct comparisons in the fibonacci heap (needed to do this since fibheap takes only 1 entry when pushing to the heap)
class PrioritizedItem:
    def __init__(self, priority, state):
        self.priority = priority
        self.state = state

    def __lt__(self, other):
        return self.priority < other.priority

# Encased fibheap fibonacci priority queue (had to add some functionality)
class FibonacciPriorityQueue:
    def __init__(self):
        # initializes fibonacci priority queue
        self.heap = fibheap.makefheap()
        self.entry_finder = {}  # dict to keep track of entries

    def add_state(self, state, priority):
        # inserts state into the queue, and stores a reference to it
        if state in self.entry_finder:
            self.remove_state(state)
        entry = PrioritizedItem(priority, state)  # Wrap the entry
        fibheap.fheappush(self.heap, entry)
        self.entry_finder[state] = entry

    def remove_state(self, state):
        # remove from queue
        entry = self.entry_finder.pop(state, None)

    def pop_state(self):
        # get min state (as sorted by actual cost or heuristic, dependent on algorithm run)
        if self.heap.num_nodes == 0:
            raise KeyError('pop from an empty priority queue')
        prioritized_item = fibheap.fheappop(self.heap)  # Unwrap the state
        state = prioritized_item.state
        del self.entry_finder[state]
        return state

    def decrease_key(self, state, new_priority):
        # decrease priority of state
        self.remove_state(state)
        self.add_state(state, new_priority)

    def __contains__(self, state):
        # check if state is in queue or not
        return state in self.entry_finder

    def __len__(self):
        # get number of states in queue
        return self.heap.num_nodes

    def is_empty(self):
        # check if queue is empty
        return self.heap.num_nodes == 0

# Pancake stack class (for calculating heuristics, getting successors, keeping track of stack, etc.)
class Pancakes:
    def __init__(self, stack, parent=None, g=0):
        self.stack = stack  # current stack of pancakes (i.e., order)
        self.parent = parent  # parent state
        self.g = g  # actual cost (backward cost)
        self.h = self.calculate_heuristic()  # forward / estimated cost
        self.f = self.g + self.h  # for A*; the total esimated cost

    def calculate_heuristic(self):
        # GAP heuristic (see README for source) for forward cost estimate; calculats # of pancakes out of place
        gaps = 0
        for i in range(len(self.stack) - 1):
            if abs(self.stack[i] - self.stack[i + 1]) > 1:
                gaps += 1
        return gaps

def flip(stack, k):
    # flips pancake stack at designated point k
    return stack[:k][::-1] + stack[k:]

def is_goal(state):
    # checks if the pancake state is at the goal state (ordered stacked pancakes, largest on bottom to smallest on top)
    return state.stack == sorted(state.stack, reverse=True)

def get_successors(state):
    # gets successors for any given state
    successors = []
    for i in range(2, len(state.stack) + 1):
        new_stack = flip(state.stack, i)
        new_state = Pancakes(new_stack, state, state.g + 1)
        successors.append(new_state)
    return successors

# Option 1: A* search for solving pancake sorting task
def a_star_search(initial_state):
    frontier = FibonacciPriorityQueue()
    frontier.add_state(initial_state, initial_state.f)
    visited = set()

    while not frontier.is_empty():  # loop through frontier while it's not empty (if it is, return None/failure)
        current_state = frontier.pop_state()  # choose a leaf node from frontier with min f(c) [= h(c) + g(c)]

        if is_goal(current_state):  # if the node contains a goal state, then . . .
            return current_state  # return the corresponding solution

        visited.add(tuple(current_state.stack))  # mark state as visited

        for child in get_successors(current_state):  # for each child of the node
            child_tuple = tuple(child.stack)
            if child_tuple not in visited and child not in frontier:  # if child is not in frontier or visited then
                frontier.add_state(child, child.f)  # insert child in frontier
            elif child in frontier:  # else if child is in frontier with higher cost then
                frontier.decrease_key(child, child.f)  # replace that frontier node with child

    return None

# Option 2: UCS for solving pancake sorting task
def uniform_cost_search(initial_state):
    frontier = FibonacciPriorityQueue()  # initialize frontier
    frontier.add_state(initial_state, initial_state.g)
    visited = set()

    while not frontier.is_empty():  # loop; if frontier is empty return None/Failure
        current_state = frontier.pop_state()  # choose a leaf node and remove it from the frontier

        # if node contains goal state, then return corresponding solution
        if is_goal(current_state):
            return current_state

        visited.add(tuple(current_state.stack))  # mark node as explored

        # expand chosen node, adding resultant nodes to frontier only if not in frontier /explored set
        for child in get_successors(current_state):
            child_tuple = tuple(child.stack)
            if child_tuple not in visited and child not in frontier:
                frontier.add_state(child, child.g)
            elif child in frontier:  # if child in frontier w/ higher cost, replace frontier node w/ child
                frontier.decrease_key(child, child.g)

    return None

# Function to print little graphic of the pancakes so we can visualize the change in pancake order at each step
def print_pancakes(stack):
    max_length = max(stack) * 2
    for pancake in reversed(stack):
        print(f"{' ' * ((max_length - pancake * 2) // 2)}{'=' * (pancake * 2)}")

# MAIN function to print an intro, facilitate user interaction, and call the chosen algorithm
def main():
    print("Welcome to the Pancake Flipper Algorithm!")
    print("This program solves the pancake sorting problem using either A* or Uniform Cost Search.")
    print("The goal is to sort a stack of pancakes from largest (10) to smallest (1).")
    print("WARNING: Please install the fibheap library via 'pip install fibheap' to run this code.")
    
    while True:
        algorithm = input("Choose the algorithm (A for A*, U for Uniform Cost Search): ").upper()
        if algorithm in ['A', 'U']:
            break
        print("Invalid choice. Please enter 'A' or 'U'.")

    while True:
        choice = input("Do you want to input your own sequence (I) or use a random one (R)? ").upper()
        if choice == 'I':
            while True:
                try:
                    stack = list(map(int, input("Enter a sequence of 10 unique numbers from 1 to 10, separated by spaces: ").split()))
                    if len(stack) != 10 or set(stack) != set(range(1, 11)):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input. Please enter 10 unique numbers from 1 to 10.")
            break
        elif choice == 'R':
            stack = list(range(1, 11))
            random.shuffle(stack)
            print("Random sequence generated:", stack)
            confirm = input("Are you okay with this sequence? (Y/N) ").upper()
            if confirm == 'Y':
                break
        else:
            print("Invalid choice. Please enter 'I' or 'R'.")

    initial_state = Pancakes(stack)
    print("\nInitial state:")
    print_pancakes(initial_state.stack)
    print(f"Stack: {initial_state.stack}")
    
    if algorithm == 'A':
        print(f"Heuristic value (forward cost): {initial_state.h}")
        solution = a_star_search(initial_state)
    else:
        solution = uniform_cost_search(initial_state)

    if solution:
        print("\nSolution found!")
        steps = []  # keep track of steps taken to find solution
        current = solution
        while current:
            steps.append(current)
            current = current.parent
        
        for i, state in enumerate(reversed(steps)):
            print(f"\nStep {i}:")
            print_pancakes(state.stack)
            print(f"Stack: {state.stack}")
            print(f"Flips performed (backward cost): {state.g}")
            if algorithm == 'A':
                print(f"Heuristic value (forward cost): {state.h}")
        
        print(f"\nTotal number of flips: {solution.g}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
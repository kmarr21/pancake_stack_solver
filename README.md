# Implementing Informed Search to Solve a Pancake Sorting Problem

## Introduction

This project implements two informed search algorithms (UCS and A* search) to solve a pancake sorting problem, in which ten pancakes of different sizes are out of order and need to be stacked in order on the plate, from largest at the bottom to smallest on top ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]). 

## Dependencies / Assumptions
- Python 3
- fibheap library (can be installed via 'pip install fibheap'); it is assumed that this is downloaded in order to run the code

## How to Run

1. Ensure you have fibheap and python 3 installed
2. Run the script: 
   ```
   python pancake.py
   ```
3. Follow the prompts to choose between A* and UCS algorithms (plus input your own pancake stack order if desired; otherwise, it will be random)

## Code Structure
- `FibonacciPriorityQueue`: wrapper class for the fibheap library; implements a fibonacci priority queue with some added functionality
- `Pancakes`: Represents a state in the pancake sorting problem (state of the pancakes)
- `a_star_search`: Implements the A* search algorithm
- `uniform_cost_search`: implements the Uniform Cost Search algorithm
- `main`: handles user interaction and code execution

## Defining the Search Problem

Here, I outline how I thought about this problem as a search problem:

### 1. Outlining the search problem:
- Initial state: unsorted stack of 10 pancakes represented by a list of integers
- Possible actions: flip the stack at any point (i.e., after 4th pancake, after 1st pancake, etc.)
- Successor function / transition model: the order of the flipped pancakes is reversed after the flip
- Goal test: pancake stack is sorted in descending order (largest to smallest)
- Path cost function: number of flips performed

### 2. Cost function (backward cost):
The backward cost (g) is defined as the number of flips performed to reach the current state from the initial state.

### 3. Heuristic function (forward cost):
The forward cost (h) uses the gap heuristic (see citation [1]), which counts the number of adjacent pancakes in the stack that are not consecutive in size. This provides an estimate of the minimum number of flips needed to sort the remaining stack.

## Notes

The UCS algorithm will (naturally) take much longer than the A* algorithm. The fibonacci heap slightly expedites this compared to my initial usage of a binary heap, but using A* is still recommended despite providing optionality for both. 

## Citations

[1] Helmert, M. (2010). Landmark Heuristics for the Pancake Problem. In Proceedings of the Third Annual Symposium on Combinatorial Search (SOCS-10) (pp. 109-110). AAAI Press.
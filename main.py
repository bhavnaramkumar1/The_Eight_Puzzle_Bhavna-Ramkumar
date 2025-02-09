# The python web was refrenced for documentation/syntax https://www.python.org/ 
#Sources for imports 
#https://docs.python.org/3/library/heapq.html
#https://docs.python.org/3/library/time.html
# Refrenced the lectures slides

import heapq #heapq is used for queue for A* and UCS 
import copy # used for deep copying state
import time # time to measure the time at the end 


#Define  goal state, 0 is used for blank 
Goal_State = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


#Class named Node to represent each node in tree 
#Refrences:https://www.geeksforgeeks.org/heuristic-search-techniques-in-ai/#1-a-search-algorithm 
class Node:
  
  def __init__(self, state, parent=None, depth=0, heuristic=0):
    self.state = state  # current 
    self.parent = parent  # parent node
    self.depth = depth   # number of moves g(n)
    self.heuristic = heuristic # cost h(n)

# total cost g(n)+h(n)
  def total_cost(self):
    return self.depth + self.heuristic
  
#less than method which lets for priority based ordering in priority queue 
  def __lt__(self, other):
    return (self.depth + self.heuristic) < (other.depth + other.heuristic)

  def __lt__(self, other):
    return self.total_cost() < other.total_cost()



#function used to find the 0 in the puzzle, the blank slot 
def find_blank_position(state):
#goes through nested loop and check if zero, if found returns postion 
  for i in range(3):
    for j in range(3):
      #if 0 found returns the row and column, if not returns none 
        if state[i][j] == 0:
            return i, j 
  return None, None


# functions make a new puzzle with the copy module at the top 
# Refrences for deepcopy: https://docs.python.org/3/library/copy.html  
def move(state, i, j, new_i, new_j):
  #creates deep copy of the state to not edit the original state 
  new_state = copy.deepcopy(state)
  #
  new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
  return new_state


#function used to expand the nodes and generate next states by moving in 4 directions 
#Refrences: https://www.geeksforgeeks.org/heuristic-search-techniques-in-ai/#1-a-search-algorithm
def expand(node):
  # lists all the valid next nodes 
  valid_nodes = []
  #finds where the 0 tile is 
  i, j = find_blank_position(node.state)
  
  moves = [
    ("Up", (i - 1, j)), # row decreases
    ("Down", (i + 1, j)), # row increases 
    ("Left", (i, j - 1)),  # column decreases 
    ("Right", (i, j + 1)) # column increases  
  ]
  
  for direction, (x, y) in moves:
      if 0 <= x < 3 and 0 <= y < 3:
        # goes through the all the directions generates new state 
        new_state = move(node.state, i, j, x, y)
        #creates new node and adds to valid nodes
        valid_nodes.append(Node(new_state, node, node.depth + 1))
  # returns all the valid nodes 
  return valid_nodes 


# counts misplaced tiles by comparing to goal state 
def misplaced_tiles(node):
  count = 0
  # nested loop goes through rows and columns 
  for i in range(3):
      for j in range(3):
        #checks if the position is the same as the goal state if not counts 1
         if node.state[i][j] != 0 and node.state[i][j] != Goal_State[i][j]:
           count += 1
           # counts and returns 
  return count


# gets the heuristic based on what user chooses
def get_heuristic(heuristic_type, node: Node):
  #if chooses 1 than hardcoded to 0
  if heuristic_type == "1":
    return 0
  #if chooses the second one goes to mispaced tiles 
  elif heuristic_type == "2":
    return misplaced_tiles(node)
  #if chooses 3 goes to manhatten node
  elif heuristic_type == "3":
    return manhattan_distance(node)
  return 0


#Refrence for manhattan distance formula:
# https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
# finds the manhattan distance 
def manhattan_distance(node):
  # initilized to 0
  distance = 0
  # goes through rows and column of the puzzle
  for i in range(len(node.state)):
    for j in range(len(node.state[i])):
      #gets the current tile and takes out the number 0 from calculation 
      current_num= node.state[i][j]
      # if not 0 
      if current_num != 0:
        # first gets rows and column where the number should be in the goal state 
        ans_x, ans_y = divmod(current_num - 1, 3)
        # distance is calculated with forumala (current row - goal row) + (current column)
        distance += abs(i - ans_x) + abs(j - ans_y)
  return distance



# function checks if the puzzle is solvabale 
#Refrence and Research to see how to check if a puzzle is solvabale 
#https://www.cs.princeton.edu/courses/archive/fall17/cos226/assignments/8puzzle/index.html#:~:text=Thus%2C%20if%20a%20board%20has,inversions%2C%20then%20it%20is%20solvable.
def check_if_solvable(state):
  # array initlized for the puzzle to be in 1d format
  one_dim = [] 
  # goes through and appends array leaving 0 out
  for row in state:
      for num in row:
          if num: 
              one_dim.append(num)
              
# initialize inverse to 0 and gets the number of tiles in puzzle 
  inverse = 0  
  n = len(one_dim)  

#inverse when large number before small number in nested loop going through the puzzle
  for i in range(n - 1):  
      for j in range(i + 1, n):  
          if one_dim[i] > one_dim[j]:  
              inverse += 1  

# if inversion is even puzzle is solvable and returns 
  return inverse % 2 == 0


#The main algorithmn performs A* or UCS based on the heuristic type 
# takes in the intital state and heuristic type

#Refrences: https://www.geeksforgeeks.org/heuristic-search-techniques-in-ai/#1-a-search-algorithm
def search_algorithm(initial_state, heuristic_type):
# initial expanded nodes and max queue size to 0 
# Variable to track the maximum size of the priority queue 
    expanded_nodes = 0
    max_queue_size = 0
    
    # check if puzzle solvable before continuing 
    if not check_if_solvable(initial_state):
        print("Puzzle not solvable!")
        return 

    # get the initial_node from the node above 
    initial_node = Node(initial_state)
    # use the user valie and assign the heurisitic
    initial_node.heuristic = get_heuristic(heuristic_type, initial_node)
    
    #check if inital state in is the goal state and returns 
    #tuple - cannot be modified after after made 
    if tuple(map(tuple, initial_state)) == tuple(map(tuple, Goal_State)):
        #1print(f"Final node reached with depth: {initial_node.depth}")
        return solution(initial_node, expanded_nodes, max_queue_size)

  
    # list
    priority_queue	 = []
    # pushes nodes to the priority_queue	 for the lowest cost node
    # pushes the cost and node into the heap 
    heapq.heappush(priority_queue,(initial_node.total_cost(), initial_node))

    #dictionary for visited states and their nodes
    explored = {}

  #loops through until goal state found or no more to explore
    while priority_queue	:
      # updating max queue size
        max_queue_size = max(max_queue_size, len(priority_queue	))

        # remove node with lowest cost similar tot greedy
        cost, node = heapq.heappop(priority_queue	)

        #convert to tuple so it can be explores
        visited_state = tuple(map(tuple, node.state))
        # if state already explored with low cost or equal than skip
        if visited_state in explored and explored[visited_state] <= node.total_cost():
            continue  # Skip worse paths to the same state
        
        # note as explored and store total cost 
        explored[visited_state] = node.total_cost()

        # if goal state than reuturn all needed for solution
        if visited_state == tuple(map(tuple, Goal_State)):  
            return solution(node, expanded_nodes, max_queue_size) 

        # expand the current node for more valid states 
        for child_node in expand(node):
          # assing heuristic value to child node 
            child_node	.heuristic = get_heuristic(heuristic_type, child_node	)
            state_tuple = tuple(map(tuple, child_node.state))

    # Check if we  found a cheaper path 
            if state_tuple in explored and explored[state_tuple] <= child_node.total_cost():
              continue  # Skip 
            # push node to prority queue for lowest cost to be expanded/ 
            heapq.heappush(priority_queue, (child_node	.total_cost(), child_node	))
            # increment expanded nodes 
            expanded_nodes += 1  


#Function to print the soltuion along with depth expanded nodes and maxqueue
def solution(node, expanded_node, max_queue):
  # makes empty list to store path before the solution 
  path = []
  while node:
      path.append(node.state)
      node = node.parent
  path.reverse()

#prints solution path, prints rows and columns 
  print("Solution Path:")
  for state in path:
      for row in state:
          print(row)
      print("---")

# prints the solution depth which is the moves taken to reach the goal
  print(f"Depth: {len(path) - 1}")
#prints total nodes expanded 
  print(f"Expanded Nodes: {expanded_node}")
# prints max queue size during the search process 
  print(f"Max Queue Size: {max_queue}")

  
  
  
  
##############################
# this functions has all the default functions stores for if the user choses them
# Source: Assignment Project 1 The_Eight_Puzzle_CS_170_2025
def default_puzzle():
  #given from the assignment instructions, difficulty based on depth level from the assignment 
  puzzles = { 
    "0": [[1, 2, 3], [4, 5, 6], [7, 8, 0]], # Depth 0
    "1": [[1, 2, 3], [4, 5, 6], [0, 7, 8]], # Depth 2
    "2": [[1, 2, 3], [5, 0, 6], [4, 7, 8]], # Depth 4
    "3": [[1, 3, 6], [5, 0, 2], [4, 7, 8]], # Depth 8
    "4": [[1, 3, 6], [5, 0, 7], [4, 8, 2]], # Depth 12
    "5": [[1, 6, 7], [5, 0, 3], [4, 8, 2]], # Depth 16
    "6": [[7, 1, 2], [4, 8, 5], [6, 3, 0]], # Depth 20
    "7": [[0, 7, 2], [4, 6, 1], [3, 5, 8]], # Depth 24
  }

  #asks for input 
  print("Default Puzzle: Choose a number between 0(easiest) to 7(hardest)")
  default_puzzle_choice = input()


# checks if user input is valid and exits if not valid 
  if default_puzzle_choice in puzzles:
    return puzzles[default_puzzle_choice]
  else:
    print("Incorrect input entered. Choose number between 0 to 7. Exiting program")
    exit()


# Inspo for user input from Assignment Project 1 The_Eight_Puzzle_CS_170_2025
# if the user chooses 2 this function runs where user can enter a 3 by 3 puzzle
def get_user_puzzle():
  print("Enter your puzzle 0-8 (0 to represent the blank slot)")
  print("Make sure each row contains 3 numbers separated by spaces. Each number should be inputted only once")

  #array to store user's puzzle in 2D
  # set helps keep track if the numbers entered are unique 
  user_puzzle = []
  all_numbers = set()

#loops to get input for 3 rows and appends 
  for i in range(3):
    row = list(map(int, input(f"Row {i+1}: ").split()))
    if len(row) != 3:
      print("Error: Each row must have 3 numbers only")
      exit()

    user_puzzle.append(row)
    all_numbers.update(row)  

#this checks if the numbers entered are from 0-8 and entered exactly once
  if all_numbers != set(range(9)): 
    print("Error: Each number should be used exactly once and be from 0 to 8")
    exit()
  return user_puzzle

# Inspo for user input from Assignment Project 1 The_Eight_Puzzle_CS_170_2025
# MAIN function where the all the user inputs are taken and program runs
def main():
  print("Hi! Welcome to the Eight Puzzle Solver")
  print("Type 1 for a selection of default puzzles or Type 2 to enter your own puzzle")

# asks user for default puzzle 1  or own puzzle 2

  puzzle_selection = input()
  
  if(puzzle_selection == "1"):
    initial_state= default_puzzle()
  elif(puzzle_selection == "2"):
    initial_state = get_user_puzzle()
  else:
    print("Invalid Input. Please Choose 1 or 2. Exiting program")
    exit()

# prints the user selected puzzle 
  print("Selected Initial State:")
  for row in initial_state:
    print(row)
  
# asks to choose to choose which algorithm to solve puzzle 
# 1 for UniformCost Search, 2 Misplaced Tile heuristic, 3 for Manhattan Distance heuristic
  print("Choose which algorithm to use to solve the puzzle. Type 1 Uniform Cost Search,Type 2 for Misplaced Tile heuristic, Type 3 for Manhattan Distance heuristic")
  algorithm_choice = input()

  if algorithm_choice in ["1", "2", "3"]:
    #after choosing used time module to start time 
    start_time = time.time()
    #passes to search algorithm function
    search_algorithm(initial_state, algorithm_choice)
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time  # Calculate elapsed time and prints 
    print(f"\nExecution Time: {elapsed_time:.6f} seconds")
  else:
    print("Invalid. Please Choose 1,2,3. Exiting program")
    exit()
  
#calls and runs main 
main()

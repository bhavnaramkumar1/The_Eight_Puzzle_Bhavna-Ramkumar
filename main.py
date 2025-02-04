import heapq
import copy


def default_puzzle():
  
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
  
  print("Default Puzzle: Choose a number between 0(easiest) to 7(hardest)")
  default_puzzle_choice = input()

  if default_puzzle_choice in puzzles:
    return puzzles[default_puzzle_choice]
  else:
    print("Incorrect input entered. Exiting program")
    exit()
     

def main():
  print("This is the eight puzzle solver" + "\n" "Type 1 for a selection of default puzzles" + "\n" + "Type 2 to enter your own ")

  puzzle_selection = input()

  if(puzzle_selection == "1"):
    initial_state= default_puzzle()
  elif(puzzle_selection == "2"):
    print("Enter your puzzle, use a zero to represent the blank")
    personal_puzzle = []
    for i in range(3):
      row = input().split(" ")
      personal_puzzle.append([int(x) for x in row])
    initial_state = personal_puzzle
  else:
    print("Incorrect input entered. Exiting program")
    exit()
  
  
main()
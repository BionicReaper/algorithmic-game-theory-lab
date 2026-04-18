import array
import random
import sys


# Game settings
misere: bool
heap_count: int
use_ai: bool

# Game parameters
num_sticks: array[int]
max_num_removed_sticks: int

# Game state
heaps: array[int]
turn = 'G' # 'G' for green and 'R' for red
winner = None

# Printing constants
ANSI_GREEN = "\033[92m"
ANSI_RED = "\033[91m"
ANSI_RESET = "\033[0m"

# Printing functions

def clear_screen():
    print("\033[2J\033[3J\033[H", end="")

def print_gamestate():
    if heap_count == 1:
        print(f"Heap: {heaps[0]}")
    else:
        for i in range(heap_count):
            print(f"Heap {i + 1}: {heaps[i]}")
    print(f"Maximum number of sticks that can be removed in one turn: {max_num_removed_sticks}")

    color = ANSI_GREEN if turn == "G" else ANSI_RED
    reset = ANSI_RESET
    print(f"Current turn player: {color}{turn}{reset}")

# Handle game logic

def swap_turn():
    global turn
    turn = 'R' if turn == 'G' else 'G'

def decrease_heap(heap_index, sticks):
    if 0 <= heap_index < heap_count and 1 <= sticks <= max_num_removed_sticks and sticks <= heaps[heap_index]:
        heaps[heap_index] -= sticks
        result = check_winner()
        if result:
            global winner
            winner = result
        swap_turn()
    else:
        print("Invalid move. Please try again.")

def check_winner():
    if all(heap == 0 for heap in heaps):
        if misere:
            return 'R' if turn == 'G' else 'G'
        else:
            return turn
        
# Handle AI logic

def ai_move():
    # Placeholder for AI logic
    pass

# Initialization functions

def input_settings():
    global misere, heap_count, use_ai

    heap_count_prompt = input("Enter the number of heaps (1 or 3): ").strip()
    while heap_count_prompt not in ["1", "3"]:
        print("Invalid input. Please enter 1 or 3.")
        heap_count_prompt = input("Enter the number of heaps (1 or 3): ").strip()
    heap_count = int(heap_count_prompt)

    if heap_count == 1:
        misere_prompt = input("Enable misere rules? (y/n): ").strip().lower()
        while misere_prompt not in ["y", "n"]:
            print("Invalid input. Please enter 'y' or 'n'.")
            misere_prompt = input("Enable misere rules? (y/n): ").strip().lower()
        misere = misere_prompt == "y"
    else:
        misere = False

    use_ai_prompt = input("Play against AI? (y/n): ").strip().lower()
    while use_ai_prompt not in ["y", "n"]:
        print("Invalid input. Please enter 'y' or 'n'.")
        use_ai_prompt = input("Play against AI? (y/n): ").strip().lower()
    use_ai = use_ai_prompt == "y"

def randomize_parameters():
    global num_sticks, max_num_removed_sticks
    if heap_count == 1:
        num_sticks = array.array('i', [random.randint(16, 25)])
    else:
        num_sticks = array.array('i', [random.randint(8, 11) for _ in range(heap_count)])
    max_num_removed_sticks = random.randint(2, 5)

def reset_game():
    global heaps
    heaps = array.array('i', num_sticks)

# Main game loop

if __name__ == "__main__":
    input_settings()
    randomize_parameters()
    reset_game()

    running = True
    valid_move = True
    while running:
        clear_screen()
        print_gamestate()

        if not use_ai or turn == 'G':
            # Player's turn
            if heap_count == 1:
                # Change the prompt if the user made an invalid choice last loop
                prompt_string = f"Enter the number of sticks to remove (1 to {min(max_num_removed_sticks, heaps[0])}): " if valid_move else f"Invalid move. You must remove between 1 and {min(max_num_removed_sticks, heaps[0])} sticks.\nEnter the number of sticks to remove: "
                move_prompt = input(prompt_string).strip()
                if move_prompt.isdigit():
                    sticks = int(move_prompt)
                    if 1 <= sticks <= min(max_num_removed_sticks, heaps[0]):
                        decrease_heap(0, sticks)
                        valid_move = True
                    else:
                        valid_move = False
                else:
                    valid_move = False
            else:
                # Change the prompt if the user made an invalid choice last loop
                prompt_string = f"Enter your move as:  <heap number>, <sticks to remove> (e.g. 1, 3 to remove 3 sticks from heap 1).\nHeap number must be between 1 and {heap_count}.\nSticks to remove must be between 1 and {max_num_removed_sticks} and less than or equal to the number of sticks in the chosen heap.\nChoice: " if valid_move else f"Invalid move. Enter your move as:  <heap number>, <sticks to remove> (e.g. 1, 3 to remove 3 sticks from heap 1).\nHeap number must be between 1 and {heap_count}.\nSticks to remove must be between 1 and {max_num_removed_sticks} and less than or equal to the number of sticks in the chosen heap.\nChoice: "
                move_prompt = input(prompt_string).strip().split(",")
                if len(move_prompt) == 2:
                    try:
                        heap, sticks = int(move_prompt[0]), int(move_prompt[1])
                        if 1 <= heap <= heap_count and 1 <= sticks <= max_num_removed_sticks and sticks <= heaps[heap - 1]:
                            decrease_heap(heap - 1, sticks)
                            valid_move = True
                        else:
                            valid_move = False
                    except ValueError:
                        valid_move = False
                else:
                    valid_move = False
        else:
            # AI's turn
            ai_move()

        if winner:
            clear_screen()
            print_gamestate()
            color = ANSI_GREEN if winner == "G" else ANSI_RED
            reset = ANSI_RESET
            print(f"Player {color}{winner}{reset} wins!")
            running = False
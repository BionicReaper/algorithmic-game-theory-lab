import sys


misere: bool

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--misere":
        if sys.argv[2].lower() == "true":
            misere = True
        elif sys.argv[2].lower() == "false":
            misere = False
        else:
            miserePrompt = input("Invalid argument for --misere. Enable misere rules? (y/n): ").strip().lower()
            misere = miserePrompt == "y"
    else:
        miserePrompt = input("Enable misere rules? (y/n): ").strip().lower()
        misere = miserePrompt == "y"

    print("tictactoe module loaded. misere =", misere)

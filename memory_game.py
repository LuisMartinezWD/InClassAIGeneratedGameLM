import random
import string
import time

LEVELS = {
    "1": ("Easy", 2, 2),
    "2": ("Medium", 4, 4),
    "3": ("Hard", 4, 6),
}


def clear_screen() -> None:
    print("\n" * 40)


def make_board(rows: int, cols: int) -> list[list[str]]:
    total_cards = rows * cols
    pair_count = total_cards // 2
    symbols = list(string.ascii_uppercase[:pair_count]) * 2
    random.shuffle(symbols)
    return [symbols[i * cols : (i + 1) * cols] for i in range(rows)]


def display_board(board: list[list[str]], revealed: set[tuple[int, int]]) -> None:
    rows = len(board)
    cols = len(board[0])

    print("    " + " ".join(f"{c+1:>2}" for c in range(cols)))
    print("   " + "---" * cols)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            if (r, c) in revealed:
                row_cells.append(f" {board[r][c]}")
            else:
                row_cells.append(" *")
        print(f"{r+1:>2} |" + "".join(row_cells))


def parse_pick(prompt: str, rows: int, cols: int, forbidden: tuple[int, int] | None = None) -> tuple[int, int]:
    while True:
        raw = input(prompt).strip()
        if raw.lower() in {"q", "quit", "exit"}:
            raise KeyboardInterrupt

        parts = raw.replace(",", " ").split()
        if len(parts) != 2:
            print("Enter row and column, for example: 2 3")
            continue

        if not all(part.isdigit() for part in parts):
            print("Please enter numbers only.")
            continue

        row, col = int(parts[0]) - 1, int(parts[1]) - 1
        if not (0 <= row < rows and 0 <= col < cols):
            print("That position is outside the board.")
            continue

        if forbidden == (row, col):
            print("You already picked that card. Choose a different one.")
            continue

        return row, col


def play_level(level_name: str, rows: int, cols: int) -> None:
    board = make_board(rows, cols)
    matched: set[tuple[int, int]] = set()
    attempts = 0
    max_matches = (rows * cols) // 2

    while len(matched) < rows * cols:
        clear_screen()
        print(f"Memory Game - {level_name}")
        print("Type q to quit at any prompt.")
        print(f"Matches found: {len(matched) // 2}/{max_matches} | Attempts: {attempts}")
        display_board(board, matched)

        first = parse_pick("First pick (row col): ", rows, cols)
        if first in matched:
            print("That card is already matched. Press Enter and choose again.")
            input()
            continue

        clear_screen()
        display_board(board, matched | {first})

        second = parse_pick("Second pick (row col): ", rows, cols, forbidden=first)
        if second in matched:
            print("That card is already matched. Press Enter and choose again.")
            input()
            continue

        attempts += 1
        reveal_now = matched | {first, second}

        clear_screen()
        display_board(board, reveal_now)

        if board[first[0]][first[1]] == board[second[0]][second[1]]:
            print("Great! It's a match.")
            matched.update({first, second})
        else:
            print("Not a match. Try to remember the positions.")

        time.sleep(1.5)

    clear_screen()
    print(f"You cleared {level_name} mode in {attempts} attempts!")


def choose_level() -> tuple[str, int, int]:
    while True:
        print("Choose difficulty:")
        for key, (name, rows, cols) in LEVELS.items():
            print(f"  {key}. {name} ({rows}x{cols})")

        choice = input("Select 1, 2, or 3: ").strip()
        if choice in LEVELS:
            return LEVELS[choice]

        print("Invalid choice.\n")


def main() -> None:
    print("Welcome to the Python Memory Game!")
    print("Match all pairs by remembering card positions.\n")

    while True:
        level_name, rows, cols = choose_level()

        try:
            play_level(level_name, rows, cols)
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            return

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            return

        clear_screen()


if __name__ == "__main__":
    main()

import random
import textwrap

HANGMAN_STAGES = [
    """
      +---+
      |   |
          |
          |
          |
     =========""",
    """
      +---+
      |   |
      O   |
          |
          |
     =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
     =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
     =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
     =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
     =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
     =========""",
]

WORD_BANK = {
    "Fruits": ["apple", "banana", "orange", "mango", "pineapple", "strawberry"],
    "Programming": ["python", "variable", "function", "algorithm", "debugging", "syntax"],
    "Animals": ["elephant", "giraffe", "dolphin", "kangaroo", "penguin", "butterfly"],
}

HINTS = {
    "apple": "A sweet fruit often used in pies.",
    "banana": "A yellow fruit that monkeys love.",
    "orange": "A citrus fruit and also a color.",
    "mango": "A tropical fruit with juicy flesh.",
    "pineapple": "A spiky tropical fruit with sweet interior.",
    "strawberry": "A small red fruit often found on short plants.",
    "python": "A popular programming language named after a comedy group.",
    "variable": "A named storage location used in programming.",
    "function": "A reusable block of code that performs a task.",
    "algorithm": "A step-by-step procedure for solving a problem.",
    "debugging": "The process of finding and fixing code errors.",
    "syntax": "The set of rules that defines valid code structure.",
    "elephant": "The largest land animal with a trunk.",
    "giraffe": "A tall animal with a long neck and spotted coat.",
    "dolphin": "A smart marine mammal known for its playful behavior.",
    "kangaroo": "A hopping marsupial native to Australia.",
    "penguin": "A flightless bird that swims in cold water.",
    "butterfly": "An insect with colorful wings that starts as a caterpillar.",
}

DIFFICULTY_SETTINGS = {
    "easy": 8,
    "medium": 6,
    "hard": 4,
}


def print_centered(message: str) -> None:
    print(textwrap.fill(message, width=70))


def choose_difficulty() -> int:
    print("Choose your difficulty:")
    for level in DIFFICULTY_SETTINGS:
        print(f"  - {level.title()} ({DIFFICULTY_SETTINGS[level]} lives)")

    while True:
        choice = input("Enter difficulty [easy/medium/hard]: ").strip().lower()
        if choice in DIFFICULTY_SETTINGS:
            return DIFFICULTY_SETTINGS[choice]
        print("Invalid choice. Please select easy, medium, or hard.")


def choose_category() -> tuple[str, list[str]]:
    print("\nPick a category:")
    for index, category in enumerate(WORD_BANK, start=1):
        print(f"  {index}. {category}")

    while True:
        choice = input("Enter category number: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(WORD_BANK):
                category = list(WORD_BANK.keys())[index - 1]
                return category, WORD_BANK[category]
        print("That is not a valid category number. Try again.")


def get_guess(guessed_letters: set[str]) -> str:
    while True:
        guess = input("Guess a letter, the full word, or type 'hint': ").strip().lower()
        if not guess:
            print("Please enter a letter, a word, or 'hint'.")
            continue
        if not guess.isalpha():
            print("Only letters are allowed. Try again.")
            continue
        if guess == "hint":
            return guess
        if len(guess) == 1 and guess in guessed_letters:
            print("You already guessed that letter. Try another one.")
            continue
        return guess


def display_game_state(display: list[str], lives: int, guessed_letters: set[str]) -> None:
    stage_index = len(HANGMAN_STAGES) - 1 - lives
    stage_index = max(0, min(stage_index, len(HANGMAN_STAGES) - 1))
    print(HANGMAN_STAGES[stage_index])
    print("\nWord:", " ".join(display))
    print("Lives left:", lives)
    print("Guessed letters:", ", ".join(sorted(guessed_letters)) if guessed_letters else "None")


def play_round() -> bool:
    print("\n" + "=" * 70)
    print_centered("Let's play Hangman! Guess letters or attempt the full word anytime.")

    category, words = choose_category()
    lives = choose_difficulty()
    chosen_word = random.choice(words)
    display = ["_"] * len(chosen_word)
    guessed_letters: set[str] = set()
    hint_used = False
    hint = HINTS.get(chosen_word, "No hint available for this word.")

    print(f"\nCategory: {category}")
    print(f"The word has {len(chosen_word)} letters.")
    print("Type 'hint' anytime if you want a clue.")

    while "_" in display and lives > 0:
        print()
        display_game_state(display, lives, guessed_letters)
        guess = get_guess(guessed_letters)

        if guess == "hint":
            if hint_used:
                print("You already used your hint for this round.")
            else:
                print(f"Hint: {hint}")
                hint_used = True
            continue

        if len(guess) == 1:
            guessed_letters.add(guess)
            if guess in chosen_word:
                for index, letter in enumerate(chosen_word):
                    if letter == guess:
                        display[index] = guess
                print(f"Nice! The letter '{guess}' appears in the word.")
            else:
                lives -= 1
                print(f"Nope — '{guess}' is not in the word.")
        else:
            if guess == chosen_word:
                display = list(chosen_word)
                break
            lives -= 1
            print(f"Wrong full-word guess. You lost one life.")

    print()
    if "_" not in display:
        print_centered(f"🎉 Congratulations! You guessed the word '{chosen_word}' correctly.")
        return True
    print_centered(f"😔 Game over. The word was '{chosen_word}'. Better luck next time!")
    return False


def ask_replay() -> bool:
    while True:
        answer = input("Play again? [y/n]: ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer with 'y' or 'n'.")


def main() -> None:
    print("🎮 Welcome to the Interactive Hangman Game!")
    wins = 0
    rounds = 0

    while True:
        rounds += 1
        if play_round():
            wins += 1
        print(f"\nScore: {wins} wins out of {rounds} rounds.")
        if not ask_replay():
            break

    print("\nThanks for playing Hangman! See you next time.")


if __name__ == "__main__":
    main()

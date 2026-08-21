## TODO
"""
 
touch menu.py

SECTION 4 - MENU & MAIN PROGRAM LOOP
OWNED BY: M-0321 (Docs / Error-Handling Lead)

YOUR TASK: Tie everything together. Build the menu, collect user input,
call the other sections in order, and handle every failure gracefully -
the program should NEVER crash, only print an error and return to the menu.
"""
from stage_1 import run_stage1
from stage_2 import run_stage2
from file_output import save_output
from datetime import datetime

def get_reviews_from_user():
    """
    Collects multi-line review input from the user until they type DONE.

    Must return:
        str: all entered lines joined together (e.g. with "\\n")
    """
    print("Enter your reviews, one per line. Type DONE when finished.")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    return "\n".join(lines)


def choose_tone():
    """
    Shows a menu asking the user to pick a reply tone.

    Must return:
        str: either "formal" or "friendly"
    """
    while True:
        print("Choose a reply tone:")
        print("1. Formal")
        print("2. Friendly")
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            return "formal"
        elif choice == "2":
            return "friendly"
        else:
            print("Invalid choice, please try again.\n")


def main_menu():
    """
    Shows the main menu (1. Analyse reviews, 2. Exit).

    Must return:
        str: the raw text the user typed (e.g. "1" or "2")
    """
    print("\nWCA Customer Feedback Analyser")
    print("1. Analyse reviews")
    print("2. Exit")
    return input("Enter your choice: ").strip()

# improve my app exist message
def get_time_based_greeting():
  """Returns 'Morning', 'Afternoon', or 'Evening' based on the current time."""
  hour = datetime.now().hour
  if 5 <= hour < 12:
    return "morning"
  elif 12 <= hour < 17:
    return "afternoon"
  else:
    return "evening"

def main():
    """
    The main program loop. Ties Sections 1-3 together via the menu.
    Must never crash - every failure path should print a message and
    return to the menu instead of raising an unhandled exception.
    """
    while True:
        try:
            choice = main_menu()

            if choice == "2":
                time_word = get_time_based_greeting()
                print(
                    f"Thank you for using WCA Customer Feedback Analyser. "
                    f"Goodbye! Have a wonderful {time_word}!"
                )
                break

            if choice != "1":
                print("Invalid choice, please try again.")
                continue

            review_text = get_reviews_from_user()

            if not review_text.strip():
                print("No reviews entered. Returning to menu.")
                continue

            stage1_result = run_stage1(review_text)

            if stage1_result is None:
                print(
                    "Something went wrong analysing the reviews. "
                    "Returning to menu."
                )
                continue

            print("\n--- Analysis Results ---")
            print(stage1_result)

            tone = choose_tone()

            reply_text = run_stage2(review_text, tone)

            if reply_text is None:
                print("Something went wrong drafting the reply.")
                reply_text = "[No reply could be generated]"

            print("\n--- Drafted Reply ---")
            print(reply_text)

            save_output(stage1_result, reply_text, tone)

        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Returning to the main menu.")
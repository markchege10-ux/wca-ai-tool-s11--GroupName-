## TODO
"""
 
touch menu.py

SECTION 4 - MENU & MAIN PROGRAM LOOP
OWNED BY: M-0321 (Docs / Error-Handling Lead)

YOUR TASK: Tie everything together. Build the menu, collect user input,
call the other sections in order, and handle every failure gracefully -
the program should NEVER crash, only print an error and return to the menu.
"""

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
    print("\n=== Main Menu ===")
    print("1. Analyse reviews")
    print("2. Exit")
    return input("Enter your choice: ").strip()


def main_loop():
    """
    The main program loop. Ties Sections 1-3 together via the menu.
    Must never crash - every failure path should print a message and
    return to the menu instead of raising an unhandled exception.
    """
    from stage_1 import run_stage1
    from stage_2 import run_stage2
    from file_output import save_output

    while True:
        choice = main_menu()

        if choice == "2":
            print("Goodbye!")
            break
        elif choice != "1":
            print("Invalid choice, please try again.")
            continue

        try:
            reviews_text = get_reviews_from_user()
            if not reviews_text.strip():
                print("No reviews entered. Returning to menu.\n")
                continue

            print("\nAnalysing reviews...")
            stage1_result = run_stage1(reviews_text)
            if stage1_result is None:
                print("Sorry, analysis failed (API error or bad response). Returning to menu.\n")
                continue

            print(f"Sentiment counts: {stage1_result['sentiment_counts']}")
            print(f"Top complaints: {', '.join(stage1_result['top_complaints'])}")
            print(f"Most negative review: {stage1_result['most_negative_review']}\n")

            tone = choose_tone()

            print("\nDrafting a reply...")
            reply_text = run_stage2(stage1_result, tone)
            if reply_text is None:
                print("Sorry, drafting the reply failed (API error). Returning to menu.\n")
                continue

            print(f"\nDrafted reply ({tone}):\n{reply_text}\n")

            save_output(stage1_result, reply_text, tone)

        except Exception as e:
            print(f"Something went wrong ({e}). Returning to menu.\n")
            continue
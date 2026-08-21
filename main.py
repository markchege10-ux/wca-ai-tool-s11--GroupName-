## TODO
"""
touch main.py

Entry point for the Feedback Analyzer tool.
Run this file to start the program: python3 main.py
Update README.md
"""

from menu import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nWCA Customer Feedback Analyser closed by user. Goodbye!")
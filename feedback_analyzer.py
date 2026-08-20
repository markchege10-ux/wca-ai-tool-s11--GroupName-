"""
feedback_analyzer.py

Entry point for the Customer Feedback Analyser.
Run this file to start the program:

    python feedback_analyzer.py

Everything else lives in its own module:
    ai_client.py   -> call_ai()                          
    stage1.py      -> build_stage1_prompt(), run_stage1()
    stage2.py      -> build_stage2_prompt(), run_stage2()
    file_output.py -> save_output()                      
    menu.py        -> all user-facing menu/input + the main loop 
"""

from menu import main_loop

if __name__ == "__main__":
    main_loop()

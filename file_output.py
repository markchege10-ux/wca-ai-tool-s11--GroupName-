"""
file_output.py

SECTION 3 - FILE SAVING
OWNED BY: M-0321 (Docs / Error-Handling Lead)

YOUR TASK: Save the results of each completed run to a file, so the user
has a record after the program closes.

Steps implemented:
  1. Make sure an "output" folder exists (create it if not - os.makedirs
     with exist_ok=True)
  2. Build a filename that includes a timestamp so runs don't overwrite
     each other (see datetime.now().strftime(...))
  3. Put together a dict with all the relevant fields (sentiment counts,
     complaints, worst review, tone used, the drafted reply)
  4. Write it to a .json file with json.dump(), wrapped in try/except
     in case the file can't be written (e.g. disk full, bad permissions)
"""

import os
import json
from datetime import datetime


def save_output(stage1_result, reply_text, tone):
    try:
        os.makedirs("output", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("output", f"run_{timestamp}.json")

        # NOTE: adjust these .get() keys if Stage 1's real dict uses
        # different field names than what's documented here.
        data = {
             "sentiment_counts": stage1_result.get("sentiment_counts"),
             "top_complaints": stage1_result.get("top_complaints"),
             "most_negative_review": stage1_result.get("most_negative_review"),
             "tone_used": tone,
             "drafted_reply": reply_text,
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Results saved to {filename}")

    except Exception as e:
        print(f"Could not save output: {e}")

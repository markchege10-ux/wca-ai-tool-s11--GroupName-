"""
--------------------------------------------------------------------------
ROLES (see "YOUR TASK" comments throughout this file):
  - Person A (Lead)              -> SECTION 0: Setup & API connector
  - Person B (Stage 1 Developer) -> SECTION 1: Analyse reviews
  - Person C (Stage 2 Developer) -> SECTION 2: Draft reply
  - Person D (Docs/Error Lead)   -> SECTION 3: File saving
                                     SECTION 4: Menu & main program loop

IMPORTANT: Each function's docstring tells you exactly what parameters it
receives and what it must return. Stick to this "contract" even though
you're writing the logic yourselves - otherwise your teammates' code won't
connect to yours. Agree on this as a group before anyone starts coding.
--------------------------------------------------------------------------
"""

import os
import json
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

# Loads variables from your local .env file (never hardcode the key itself)
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


# =============================================================================
# SECTION 0 - SETUP & API CONNECTOR
# OWNED BY: Person A (markchege10-ux)
#
# YOUR TASK: Write the function that actually talks to the Groq API.
# This is the shared engine both Stage 1 and Stage 2 will call, so build
# and test this FIRST, before Person B/C start their sections - they can't
# test anything without it working.
# =============================================================================
def call_ai(messages, force_json=False):
    """
    Sends a single request to the Groq chat completions endpoint.

    Parameters:
        messages (list): A list of dicts like
            [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
        force_json (bool): If True, tells the API to guarantee valid JSON output.

    Must return:
        str: the AI's reply text, on success
        None: if the call fails for any reason (missing key, network error,
              bad response) - callers rely on None to know something went wrong
    """
    if not API_KEY:
        print("ERROR: No API key found. Check your .env file has GROQ_API_KEY set.")
        return None

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.4,
    }

    if force_json:
        payload["response_format"] = {"type": "json_object"}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"ERROR: API call failed ({e}). Check your internet connection or API key.")
        return None
    except (KeyError, IndexError):
        print("ERROR: Unexpected response shape from the API.")
        return None


# =============================================================================
# SECTION 1 - STAGE 1: ANALYSE REVIEWS
# OWNED BY: EVA-247 (Stage 1 Developer)
# =============================================================================
def build_stage1_prompt(reviews_text):
    """
    Builds the R-T-C-C-O prompt for Stage 1.

    Parameters:
        reviews_text (str): the raw block of customer reviews pasted by the user

    Must return:
        list: messages in the format [{"role": "system", ...}, {"role": "user", ...}]

    Your JSON output schema must exactly match this shape, since Stage 2
    (Person C) depends on these exact key names:
        {
          "sentiment_counts": {"positive": 0, "neutral": 0, "negative": 0},
          "top_complaints": ["theme1", "theme2"],
          "most_negative_review": "verbatim text of the worst review"
        }
    """
    system_prompt = (
        "You are an expert customer review analyst. Analyse the provided "
        "customer reviews, and extract sentiment counts, top recurring "
        "complaints, and identify the single most negative review. The "
        "reviews are informal and may contain a mix of English and Sheng. "
        "Provide the output as a raw JSON object in the exact format "
        "specified, with a maximum of 3 complaint themes and one worst "
        "review. You MUST use these exact keys: 'sentiment_counts', "
        "'top_complaints', and 'most_negative_review'."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": reviews_text},
    ]
    return messages


def run_stage1(reviews_text):
    """
    Runs Stage 1 end to end: builds the prompt, calls the AI, parses the result.

    Parameters:
        reviews_text (str): the raw block of customer reviews

    Must return:
        dict: parsed JSON matching the schema above, on success
        None: if the API call failed or the response wasn't valid/expected JSON
    """
    messages = build_stage1_prompt(reviews_text)
    raw_response = call_ai(messages, force_json=True)
    if raw_response is None:
        return None
    try:
        data = json.loads(raw_response)
    except Exception:
        return None
    required_keys = ["sentiment_counts", "top_complaints", "most_negative_review"]
    if all(key in data for key in required_keys):
        return data
    return None


# =============================================================================
# SECTION 2 - STAGE 2: DRAFT A REPLY
# OWNED BY: Paulinendugi-eng (Stage 2 Developer)
#
# YOUR TASK: Build the prompt that drafts a reply to the worst review, using
# Stage 1's output as input. Build the function that calls it.
# =============================================================================
def build_stage2_prompt(most_negative_review, complaints, tone):
    """
    Builds the R-T-C-C-O prompt for Stage 2.

    Parameters:
        most_negative_review (str): the worst review text, from Stage 1's output
        complaints (list): list of complaint theme strings, from Stage 1's output
        tone (str): either "formal" or "friendly" - controls the reply's tone

    Must return:
        list: messages in the format [{"role": "system", ...}, {"role": "user", ...}]
    """
    # TODO: Person C - implement this function
    pass


def run_stage2(stage1_result, tone):
    """
    Runs Stage 2 end to end: builds the prompt from Stage 1's result, calls the AI.

    Parameters:
        stage1_result (dict): the dict returned by run_stage1() - use its
            "most_negative_review" and "top_complaints" keys
        tone (str): "formal" or "friendly", chosen by the user in the menu

    Must return:
        str: the drafted reply text, on success
        None: if the API call failed
    """
    # TODO: Person C - implement this function
    pass


# =============================================================================
# SECTION 3 - FILE SAVING
# OWNED BY: M-0321 (Docs / Error-Handling Lead)
# =============================================================================
def save_output(stage1_result, reply_text, tone):
    """
    Saves one completed run's results to a timestamped .json file in output/.

    Parameters:
        stage1_result (dict): Stage 1's result dict
        reply_text (str): Stage 2's drafted reply (or a placeholder string
            if Stage 2 failed)
        tone (str): the tone that was used ("formal" or "friendly")

    Must return: nothing required, but should not crash the program if
    saving fails - handle errors and print a message instead.
    """
    # TODO: Person D - implement this function
    pass


# =============================================================================
# SECTION 4 - MENU & MAIN PROGRAM LOOP
# OWNED BY: M-0321 (Docs / Error-Handling Lead)
# =============================================================================
def get_reviews_from_user():
    """
    Collects multi-line review input from the user until they type DONE.

    Must return:
        str: all entered lines joined together (e.g. with "\\n")
    """
    # TODO: Person D - implement this function
    pass


def choose_tone():
    """
    Shows a menu asking the user to pick a reply tone.

    Must return:
        str: either "formal" or "friendly"
    """
    # TODO: Person D - implement this function
    pass


def main_menu():
    """
    Shows the main menu (1. Analyse reviews, 2. Exit).

    Must return:
        str: the raw text the user typed (e.g. "1" or "2")
    """
    # TODO: Person D - implement this function
    pass


def main():
    """
    The main program loop. Ties Sections 1-3 together via the menu.
    Must never crash - every failure path should print a message and
    return to the menu instead of raising an unhandled exception.
    """
    # TODO: Person D - implement this function
    pass


if __name__ == "__main__":
    main()

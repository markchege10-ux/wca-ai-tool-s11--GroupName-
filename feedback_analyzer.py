"""
Customer Feedback Analyser
WeCan Academy - AI Course, Season 11 - End of Module Project

A two-stage AI-powered tool:
  Stage 1: Analyses a batch of customer reviews -> sentiment counts + top
           recurring complaints + identifies the single most negative review.
  Stage 2: Drafts a professional reply to that most negative review, in a
           tone the user chooses from a menu (Formal / Friendly).

Group: [Your Group Name Here]
Members: [Add all 4 names here]

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
#
# Steps to research and implement:
#   1. Build the request headers (needs "Authorization: Bearer <API_KEY>"
#      and "Content-Type: application/json")
#   2. Build the JSON payload: model, messages, temperature
#      (add "response_format": {"type": "json_object"} when force_json=True)
#   3. Send a POST request to API_URL using the `requests` library
#   4. Handle failures with try/except (bad key, no internet, timeout)
#   5. Pull the actual reply text out of the response and return it
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
    # TODO: Person A - implement this function
    pass


# =============================================================================
# SECTION 1 - STAGE 1: ANALYSE REVIEWS
# OWNED BY: EVA-247 (Stage 1 Developer)
#
# YOUR TASK: Build the prompt that gets sent to the AI for Stage 1, and the
# function that calls it and safely parses the result.
#
# Steps to implement build_stage1_prompt():
#   1. Write a system_prompt using R-T-C-C-O:
#        Role       - who is the AI? (e.g. a customer insights analyst)
#        Task       - what should it do? (classify sentiment, find complaints)
#        Context    - reviews may be informal / mix English and Sheng
#        Constraints- max 3 complaint themes, JSON only, one worst review
#        Output     - give it the EXACT JSON shape you want back (see below)
#   2. Return a list of two dicts: {"role": "system", ...} and {"role": "user", ...}
#      (the user message should contain the actual reviews_text)
#
# Steps to implement run_stage1():
#   1. Call build_stage1_prompt(reviews_text) to get your messages
#   2. Pass them to call_ai(messages, force_json=True)
#   3. If call_ai returned None, return None
#   4. Try to json.loads() the result - wrap in try/except for bad JSON
#   5. Check the parsed dict actually has the 3 keys you expect
#   6. Return the parsed dict (or None if anything above failed)
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
    # TODO: Person B - implement this function
    system_prompt=("you are an expert customer review analyst.Analyse the provided customer reviews, and extract"
    " sentiment counts, top recurring complaints, and identify the single most negative review. The reviews are"
    " informal and may contain a mix of English and Sheng. Please provide the output as a raw json object in the exact "
    "JSON format specified"
    "  with a maximum of 3 complaint themes and one worst review."you MUST use this exact keys:''
    'sentiment_counts', 'top_complaints', and 'most_negative_review'."
 )
    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": reviews_text}
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
    # TODO: Person B - implement this function
    pass


# =============================================================================
# SECTION 2 - STAGE 2: DRAFT A REPLY
# OWNED BY: Paulinendugi-eng (Stage 2 Developer)
#
# YOUR TASK: Build the prompt that drafts a reply to the worst review, using
# Stage 1's output as input. Build the function that calls it.
#
# Steps to implement build_stage2_prompt():
#   1. Write a system_prompt using R-T-C-C-O:
#        Role       - a professional, empathetic customer service rep
#        Task       - write a reply to the worst review
#        Context    - the review text + complaint themes from Stage 1
#        Constraints- under 150 words, one apology, one concrete next step,
#                     no generic corporate filler, tone depends on `tone` param
#        Output     - plain text reply only
#   2. Use the `tone` parameter ("formal" or "friendly") to change the
#      instruction you give the AI (e.g. via an if/else or a small dict)
#   3. Return a list of two dicts, same shape as Stage 1
#
# Steps to implement run_stage2():
#   1. Pull most_negative_review and top_complaints out of stage1_result
#   2. Call build_stage2_prompt() with those plus the tone
#   3. Pass the messages to call_ai(messages, force_json=False)
#   4. Return whatever call_ai gives you (text or None)
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
#
# YOUR TASK: Save the results of each completed run to a file, so the user
# has a record after the program closes.
#
# Steps to implement:
#   1. Make sure an "output" folder exists (create it if not - os.makedirs
#      with exist_ok=True)
#   2. Build a filename that includes a timestamp so runs don't overwrite
#      each other (see datetime.now().strftime(...))
#   3. Put together a dict with all the relevant fields (sentiment counts,
#      complaints, worst review, tone used, the drafted reply)
#   4. Write it to a .json file with json.dump(), wrapped in try/except
#      in case the file can't be written (e.g. disk full, bad permissions)
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
#
# YOUR TASK: Tie everything together. Build the menu, collect user input,
# call the other sections in order, and handle every failure gracefully -
# the program should NEVER crash, only print an error and return to the menu.
#
# Steps to implement:
#   get_reviews_from_user() - loop on input(), collecting lines until the
#       user types "DONE", then join them into one string
#   choose_tone() - print a small menu (1=Formal, 2=Friendly), return the
#       matching string ("formal"/"friendly") based on what the user typed
#   main_menu() - print the top-level menu (1=Analyse, 2=Exit), return
#       the user's raw choice
#   main() - the main while-loop:
#       1. Show main_menu(), handle "2" (exit) and invalid choices
#       2. Call get_reviews_from_user() - if empty, print error, loop again
#       3. Call run_stage1() - if it returns None, print error, loop again
#       4. Print Stage 1's results nicely
#       5. Call choose_tone()
#       6. Call run_stage2() - if it returns None, still save what you have
#          and print an error, then loop again
#       7. Print the drafted reply
#       8. Call save_output() with everything
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

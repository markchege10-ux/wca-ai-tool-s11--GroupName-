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
"""

import os
import json
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# SETUP: Load API key securely from .env (never hardcode it in the script)
# ---------------------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


def call_ai(messages, force_json=False):
    """
    Sends a single request to the Groq chat completions endpoint.
    Returns the assistant's text reply as a string, or None on failure.

    messages: list of {"role": "system"/"user", "content": "..."} dicts
    force_json: if True, asks the API to guarantee valid JSON output
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
        # Covers no internet, timeout, bad status codes, etc.
        print(f"ERROR: API call failed ({e}). Check your internet connection or API key.")
        return None
    except (KeyError, IndexError):
        print("ERROR: Unexpected response shape from the API.")
        return None


# ---------------------------------------------------------------------------
# STAGE 1: Analyse reviews -> sentiment + complaints (JSON output)
# ---------------------------------------------------------------------------
def build_stage1_prompt(reviews_text):
    """
    R-T-C-C-O breakdown for Stage 1:
      Role       - customer insights analyst
      Task       - classify sentiment + extract recurring complaints
      Context    - raw, informal reviews (may mix English/Sheng, WhatsApp style)
      Constraints- max 3 complaint themes, valid JSON only, pick ONE most negative review
      Output     - strict JSON schema defined below
    """
    system_prompt = (
        "You are a customer insights analyst for a small Kenyan business. "
        "You will be given a batch of raw customer reviews, which may be informal, "
        "short, or mix English and Sheng. Your task is to classify the sentiment "
        "of each review, identify at most 3 recurring complaint themes, and select "
        "the single most negative review verbatim.\n\n"
        "Respond with ONLY valid JSON in exactly this shape, no extra commentary:\n"
        "{\n"
        '  "sentiment_counts": {"positive": 0, "neutral": 0, "negative": 0},\n'
        '  "top_complaints": ["theme1", "theme2"],\n'
        '  "most_negative_review": "verbatim text of the worst review"\n'
        "}"
    )
    user_prompt = f"Here are the customer reviews:\n\n{reviews_text}"
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def run_stage1(reviews_text):
    """Calls the AI, parses JSON safely, returns a dict or None."""
    messages = build_stage1_prompt(reviews_text)
    raw_output = call_ai(messages, force_json=True)

    if raw_output is None:
        return None

    try:
        parsed = json.loads(raw_output)
        # Basic sanity check on the schema we expect back
        required_keys = {"sentiment_counts", "top_complaints", "most_negative_review"}
        if not required_keys.issubset(parsed.keys()):
            print("ERROR: AI response was valid JSON but missing expected fields.")
            return None
        return parsed
    except json.JSONDecodeError:
        print("ERROR: AI did not return valid JSON. Try again.")
        return None


# ---------------------------------------------------------------------------
# STAGE 2: Draft a reply to the most negative review (uses Stage 1's output)
# ---------------------------------------------------------------------------
def build_stage2_prompt(most_negative_review, complaints, tone):
    """
    R-T-C-C-O breakdown for Stage 2:
      Role       - professional customer service representative
      Task       - write a reply to the worst review
      Context    - the review text + complaint themes from Stage 1
      Constraints- under 150 words, acknowledge issue, one apology, concrete next step
      Output     - plain text reply, tone set by user's menu choice
    """
    tone_instruction = {
        "formal": "Use a formal, professional tone suitable for an official email.",
        "friendly": "Use a warm, friendly tone suitable for a WhatsApp or SMS reply.",
    }[tone]

    system_prompt = (
        "You are a professional, empathetic customer service representative "
        "for a small Kenyan business. Write a reply to the customer's review below. "
        f"{tone_instruction} "
        "Keep the reply under 150 words. Acknowledge the specific issue raised, "
        "apologise once (do not over-apologise), and offer one concrete next step. "
        "Avoid generic corporate filler language. Respond with the reply text only."
    )
    user_prompt = (
        f"Most negative review: \"{most_negative_review}\"\n"
        f"Known recurring complaint themes: {', '.join(complaints)}"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def run_stage2(stage1_result, tone):
    """Feeds Stage 1's output into Stage 2. Returns reply text or None."""
    messages = build_stage2_prompt(
        stage1_result["most_negative_review"],
        stage1_result["top_complaints"],
        tone,
    )
    return call_ai(messages, force_json=False)


# ---------------------------------------------------------------------------
# FILE SAVING: keeps a copy of every completed run
# ---------------------------------------------------------------------------
def save_output(stage1_result, reply_text, tone):
    """Saves the full result of a run to a timestamped .json file."""
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join("output", f"analysis_{timestamp}.json")

    record = {
        "timestamp": timestamp,
        "sentiment_counts": stage1_result["sentiment_counts"],
        "top_complaints": stage1_result["top_complaints"],
        "most_negative_review": stage1_result["most_negative_review"],
        "reply_tone": tone,
        "drafted_reply": reply_text,
    }

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
        print(f"\nSaved to {filepath}")
    except OSError as e:
        print(f"ERROR: Could not save file ({e}).")


# ---------------------------------------------------------------------------
# MENU / MAIN PROGRAM LOOP
# ---------------------------------------------------------------------------
def get_reviews_from_user():
    """
    Collects multi-line review input from the user.
    User pastes reviews (one per line) and types DONE on its own line to finish.
    """
    print("\nPaste your customer reviews below, one per line.")
    print("Type DONE on its own line when finished.\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    return "\n".join(lines)


def choose_tone():
    """Menu for Stage 2 tone selection - satisfies the 'menu with 2+ choices' requirement."""
    print("\nHow should the reply be written?")
    print("  1. Formal (email style)")
    print("  2. Friendly (WhatsApp/SMS style)")
    choice = input("Enter 1 or 2: ").strip()
    return "formal" if choice == "1" else "friendly"


def main_menu():
    print("=" * 55)
    print("   CUSTOMER FEEDBACK ANALYSER")
    print("=" * 55)
    print("1. Analyse a batch of reviews")
    print("2. Exit")
    return input("Choose an option: ").strip()


def main():
    while True:
        choice = main_menu()

        if choice == "2":
            print("Goodbye!")
            sys.exit(0)

        if choice != "1":
            print("Invalid option. Please choose 1 or 2.\n")
            continue

        reviews_text = get_reviews_from_user()

        # ERROR HANDLING: empty input
        if not reviews_text.strip():
            print("ERROR: No reviews entered. Returning to menu.\n")
            continue

        print("\nAnalysing reviews...")
        stage1_result = run_stage1(reviews_text)

        # ERROR HANDLING: Stage 1 failed (bad API call or invalid JSON)
        if stage1_result is None:
            print("Could not complete analysis. Returning to menu.\n")
            continue

        print("\n--- STAGE 1 RESULTS ---")
        print(f"Sentiment counts: {stage1_result['sentiment_counts']}")
        print(f"Top complaints: {', '.join(stage1_result['top_complaints'])}")
        print(f"Most negative review: \"{stage1_result['most_negative_review']}\"")

        tone = choose_tone()

        print("\nDrafting reply...")
        reply_text = run_stage2(stage1_result, tone)

        # ERROR HANDLING: Stage 2 failed
        if reply_text is None:
            print("Could not draft a reply. Analysis results were still generated above.\n")
            save_output(stage1_result, "N/A - reply generation failed", tone)
            continue

        print("\n--- STAGE 2: DRAFTED REPLY ---")
        print(reply_text)

        save_output(stage1_result, reply_text, tone)
        print()


if __name__ == "__main__":
    main()

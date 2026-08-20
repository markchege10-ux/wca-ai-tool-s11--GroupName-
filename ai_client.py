import os

import requests
from dotenv import load_dotenv

# Loads variables from your local .env file (never hardcode the key itself)
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"  # heads up: check this hasn't been deprecated on Groq's end


# =============================================================================
# SECTION 0 - SETUP & API CONNECTOR
# OWNED BY: Person A (markchege10-ux)
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
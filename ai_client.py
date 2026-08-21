import requests

from config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL

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

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.4,
    }

    if force_json:
        payload["response_format"] = {"type": "json_object"}

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )

        if not response.ok:
            print(f"ERROR: Groq API returned HTTP {response.status_code}")

            try:
                print("Groq error:", response.json())
            except ValueError:
                print("Groq response:", response.text)

            return None

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        print("ERROR: Groq API request timed out.")
        return None

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to Groq.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}")
        return None

    except (KeyError, IndexError, TypeError, ValueError) as e:
        print(f"ERROR: Unexpected Groq response: {e}")
        return None
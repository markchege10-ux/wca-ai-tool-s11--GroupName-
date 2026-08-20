import json

from ai_client import call_ai


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
    except (json.JSONDecodeError, TypeError):
        return None
    required_keys = ["sentiment_counts", "top_complaints", "most_negative_review"]
    if all(key in data for key in required_keys):
        return data
    return None
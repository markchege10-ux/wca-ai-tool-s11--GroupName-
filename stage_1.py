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

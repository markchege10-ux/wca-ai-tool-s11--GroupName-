from ai_client import call_ai
from stage_1 import run_stage1

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
    system_prompt = (
         "You are a professional customer service representative responding "
         "on behalf of a small Kenyan business. "
         "Write a reply to the customer's review below. "
         "Rules: keep the reply under 150 words, acknowledge the issue, "
         "apologise exactly once, offer one clear next step, never blame the "
         "customer, and don't sound robotic. "
         f"Tone: {tone}. "
         "If the tone is 'friendly', sound warm and conversational. "
         "If the tone is 'formal', sound professional and respectful. "
         "Output plain text only — no JSON, no markdown, no headers."  # Output
    )

    user_prompt = (
        f"Most negative review:\n{most_negative_review}\n\n"
        f"Top complaints:\n{', '.join(complaints)}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return messages


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

    if stage1_result is None:
        print("ERROR: Stage 1 failed. No data was returned.")
        return None

    if "most_negative_review" not in stage1_result:
        print("ERROR: Stage 1 result is missing 'most_negative_review'.")
        print("Stage 1 result:", stage1_result)
        return None

    if "top_complaints" not in stage1_result:
        print("ERROR: Stage 1 result is missing 'top_complaints'.")
        print("Stage 1 result:", stage1_result)
        return None

    most_negative_review = stage1_result["most_negative_review"]
    top_complaints = stage1_result["top_complaints"]

    messages = build_stage2_prompt(
        most_negative_review,
        top_complaints,
        tone
    )

    return call_ai(messages)
def build_stage2_prompt(most_negative_review, top_complaints, tone):
    prompt = f"""
    You are a professional customer service representative.
    Write a reply to this customer's  review:
    
    Most negative review:
    {most_negative_review}
    
    Top complaints:
    {top_complaints}
    
    Tone:
    {tone}
    
    Rules:
    - Keep the reply under 150 words.
    -Acknowledge the issue.
    -Apologise once.
    -Offer a clear next step.
    -Do not blame the customer.
    -Do not sound robotic.
    -If the tone is Friendly, sound warm and conversational.
    -If the tone is Formal, sound professional and respectful.
    """
    return prompt


def run_stage2(stage1_result, tone):
    most_negative_review = stage1_result["most_negative_review"]
    top_complaints = stage1_result["top_complaints"]

    prompt = build_stage2_prompt(most_negative_review, top_complaints, tone)
    response = call_ai(prompt)
    return response 


stage1_result = {
    "most_negative_review": "The food arrived late and was cold.",
    "top_complaints": ["Late delivery", "Cold food"]
}
result = run_stage2(stage1_result, "friendly")
print(result)

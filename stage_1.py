import json
from feedback_analyzer import call_ai,build_stage1_prompt

def run_stage1(review_text):
 
 messages =build_stage1_prompt(review_text)

 raw_response=call_ai  (messages, force_json=True)
 if raw_response is None:
  return None

 try:
  data = json.loads(raw_response)
 except Exception:
  return None

required_keys =["sentiment_counts","top_complaints","most_negative_review"]
if all(key in data for key in required_keys):
    return data

     return None


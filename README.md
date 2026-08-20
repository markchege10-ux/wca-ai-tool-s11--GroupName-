# Customer Feedback Analyser

An AI-powered tool that analyses batches of customer reviews and drafts a
reply to the most negative one. Built for the WeCan Academy AI Course,
Season 11 End of Module Project.

## What it does

**Stage 1 — Analyse:** Paste in 5–10 customer reviews (or WhatsApp
messages). The tool sends them to an AI model, which returns:
- A sentiment count (positive / neutral / negative)
- Up to 3 recurring complaint themes
- The single most negative review

**Stage 2 — Reply:** Using Stage 1's output, the tool drafts a
professional reply to that worst review, in a tone you choose
(Formal or Friendly).

Every completed run is saved as a timestamped JSON file in `output/`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Get a free Groq API key from https://console.groq.com/keys

3. Create a `.env` file in the project folder (copy `.env.example`)
   and add your key:
   ```
   GROQ_API_KEY=your_real_key_here
   ```
   **Never commit your real `.env` file.** It's already excluded in
   `.gitignore`.

## Running the tool

```
python feedback_analyzer.py
```

Follow the on-screen menu:
1. Choose "Analyse a batch of reviews"
2. Paste reviews, one per line, then type `DONE`
3. Review the sentiment/complaint breakdown
4. Choose a reply tone (Formal or Friendly)
5. Read the drafted reply — it's automatically saved to `output/`

## AI Instruction Design (R-T-C-C-O)

**Stage 1 prompt**
- Role: customer insights analyst for a small Kenyan business
- Task: classify sentiment, extract complaint themes, flag worst review
- Context: informal, possibly mixed-language reviews
- Constraints: max 3 complaint themes, valid JSON only
- Output: fixed JSON schema (see `build_stage1_prompt` in the code)

**Stage 2 prompt**
- Role: professional, empathetic customer service representative
- Task: draft a reply to the flagged worst review
- Context: the review text + complaint themes from Stage 1
- Constraints: under 150 words, one apology, one concrete next step
- Output: plain text reply, tone controlled by user's menu choice

## Error handling covered

- Empty input at the review-paste stage
- API call failure (no internet, bad key, timeout)
- Malformed / invalid JSON returned by the model
- Stage 2 failure after a successful Stage 1 (partial results still saved)

## Team

- Group name: _fill in_
- Members: _fill in all 4 names + GitHub usernames_

- Group name: _fill in_
- Members: _fill in all 4 names + GitHub usernames_


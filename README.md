# Customer Feedback Analyser

An AI-powered tool that analyses batches of customer reviews and drafts a
reply to the most negative one. Built for the WeCan Academy AI Course,
Season 11 End of Module Project.

## What it does

**Stage 1 — Analyse:** Paste in 5–10 customer reviews (or WhatsApp messages). The tool sends them to an AI model, which returns:

- A sentiment count (positive / neutral / negative)
- Up to 3 recurring complaint themes
- The single most negative review

**Stage 2 — Reply:** Using Stage 1's output, the tool drafts a professional reply to that worst review, in a tone you choose:

- Formal
- Friendly

Every completed run is saved as a timestamped JSON file in `output/`.

## Project Structure

```bash
WCA-AI-TOOLL-S11-GROUP/
│
├── main.py
├── menu.py
├── ai_client.py
├── config.py
├── file_output.py
├── stage_1.py
├── stage_2.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Makefile
├── README.md
├── feedback_analyzer.py
├── screenshots/
└── output/
    └── feedback_analysis_2026-08-21_08-30-00.json
```
## Requirements

Before running the project, make sure you have:

- Python 3 installed
- `make` installed
- A Groq API key and Model
- Internet access for the AI API calls

The project uses a Python virtual environment so that its dependencies remain isolated from the system Python installation.

## Setup

### 1. Install dependencies

The project includes a `Makefile` to simplify setup.

Run:

```bash
make install
```
This command:

1. Creates a virtual environment in ``.venv``
2. Upgrades ``pip``
3. Installs all dependencies from ```requirements.txt```

You can also run:
```bash
make setup
```
``make setup`` is an alias for the installation process.

### 2. Configure the Groq API

Get a free Groq API key from:

https://console.groq.com/keys

Copy .env.example to .env:

```bash
cp .env.example .env
```

Then add your Groq configuration to the .env file:

```bash
GROQ_API_KEY=your_real_key_here
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
GROQ_MODEL=openai/gpt-oss-20b
```

### Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |
| `GROQ_API_URL` | Groq API endpoint used for chat completions |
| `GROQ_MODEL` | AI model used by the application |

**Important:** Replace `your_real_key_here` with your actual Groq API key and Model defined in Groq.

**Never commit your real `.env` file.** It should remain excluded through `.gitignore`.

### 3. Run the application

After completing the setup, run:
```bash
make run
```

The application uses the Python interpreter inside the .venv virtual environment.

Follow the on-screen menu:
1. Choose "Analyse a batch of reviews"
2. Paste reviews, one per line
3. Type DONE when you have finished entering reviews
4. Review the sentiment and complaint breakdown
5. Choose a reply tone: Formal or Friendly
6. Read the AI-generated response
7. The completed results are automatically saved to output/

You can also run the application directly with:
 ```bash 
 .venv/bin/python main.py
 ```

 ### Makefile Commands
The project provides the following commands:
| Command        | Description                                               |
| -------------- | --------------------------------------------------------- |
| `make install` | Creates the virtual environment and installs dependencies |
| `make setup`   | Runs the installation/setup process                       |
| `make run`     | Runs the Customer Feedback Analyser                       |
| `make clean`   | Removes the virtual environment and Python cache          |

For Example
```sh
make setup
make run
```

To reset the local environment:

```sh
make clean
```

## AI Instruction Design — R-T-C-C-O

The prompts used by the application follow the R-T-C-C-O approach: Role, Task, Context, Constraints, Output.

**Stage 1 prompt**

- Role:
    Customer insights analyst for a small Kenyan business.

- Task:
    Classify the sentiment of customer feedback, identify recurring complaint themes, and flag the worst review.

- Context:
    Reviews may be informal, conversational, or contain mixed-language content.

- Constraints:
    - Identify sentiment as positive, neutral, or negative
    - Return a maximum of 3 complaint themes
    - Identify the single most negative review
    - Return valid JSON only

- Output:
    A fixed JSON schema used by the application. (See `build_stage1_prompt` in the source code).

**Stage 2 prompt**

- Role:
    Professional and empathetic customer service representative.

- Task:
    Draft a response to the worst customer review identified during Stage 1.

- Context:
    The prompt includes the original review and the complaint themes identified during analysis.

- Constraints:
    - Keep the response under 150 words
    - Include one apology
    - Include one concrete next step
    - Follow the tone selected by the user

- Output:
    A plain text reply, tone controlled by user's menu choice.

## Error Handling

The application handles several common failure scenarios:

- Empty input during the review-paste stage
- API call failures, including connection problems, invalid API keys, and timeouts
- Malformed or invalid JSON returned by the AI model
- Stage 2 failures after Stage 1 has completed
(Partial results are still saved when Stage 2 fails)

## Example Output

A successful run produces analysis results such as:
```json
{
    "sentiment_counts": {
        "positive": 1,
        "negative": 1,
        "neutral": 0
    },
    "top_complaints": [
        "slow service",
        "cold food"
    ],
    "most_negative_review": "The service was too slow and my supu was cold. Very disappointed!",
    "tone_used": "formal",
    "drafted_reply": "[No reply could be generated]"
}
```

The completed run is also saved as a timestamped JSON file inside:

```
output/
├── feedback_analysis_2026-08-20_08-30-00.json
└── feedback_analysis_2026-08-21_08-12-45.json
```
The JSON output contains the analysis results and generated response from the completed run.

### Example Workflow

A user can enter reviews such as:

```sh
The food was amazing and delivery was very fast.

My order arrived late and the food was already cold.

The customer service was okay but I waited too long for my order.

I really enjoyed the food. Will definitely order again.

Very disappointing experience. My order was late and nobody answered my calls.
```

The AI then analyses the reviews and produces information such as:
```json 
    Sentiment:
        Positive: 2 
        Neutral: 1
        Negative: 2


    Recurring Complaint Themes:
        1. Late delivery
        2. Poor communication
        3. Food arriving cold


    Most Negative Review: 
        "Very disappointing experience. My order was late and nobody answered my calls."

```

The user can then select a response tone and receive an AI-generated customer service reply.

### Successful Results

The application has been successfully tested.

The screenshot below shows a successful execution of the Customer Feedback Analyser, including the analysis results and generated customer response.

Screenshot — Successful Analysis

![Successful analysis results](<screenshots/success analysis.png>)

![Successful app exit](<screenshots/app exit.png>)

Note: Save the screenshot in the project as screenshots/successful analysis.png, or update the image path above to match the actual filename.

### Graceful Exit

The application allows users to exit safely from the terminal menu.

If the user selects **Exit**, the application displays a goodbye message and closes normally.

The application also handles `Ctrl+C` (`KeyboardInterrupt`) so that users can stop the program without receiving an unnecessary Python traceback.

Example:

```text
WCA Customer Feedback Analyser

1. Analyse reviews
2. Exit

Enter your choice: ^X^C

WCA Customer Feedback Analyser closed by user. Goodbye!
```

### Team
- Group name: wca-ai-tool-s11-Group
- Members:
```shh
    Member 1 — markchege10-ux
    Member 2 — EVA-247
    Member 3 — paulinendugi-eng
    Member 4 — M-0321
```
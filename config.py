from dotenv import load_dotenv
import os

# Loads variables from your local .env file (never hardcode the key itself)
load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"{name} is not set")

    return value


GROQ_API_KEY = get_required_env("GROQ_API_KEY")
GROQ_API_URL = get_required_env("GROQ_API_URL")
GROQ_MODEL = get_required_env("GROQ_MODEL") # heads up: check this hasn't been deprecated on Groq's end

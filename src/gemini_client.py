import os

from dotenv import load_dotenv
from google import genai


# Load variables from .env
load_dotenv()


# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not set. "
        "Please add it to the .env file."
    )


# Create Gemini client
client = genai.Client(
    api_key=GOOGLE_API_KEY
)
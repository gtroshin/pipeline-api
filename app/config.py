import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError(
        "No API_KEY set for Flask application. Please set API_KEY environment variable."
    )

import os
from pathlib import Path

from dotenv import load_dotenv


# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent



# Environment Variables
load_dotenv(BASE_DIR / ".env")


# Ollama Configuration

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
).rstrip("/")


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:latest"
)


# Chat Configuration
MAX_RECENT_MESSAGES = int(
    os.getenv(
        "MAX_RECENT_MESSAGES",
        "12"
    )
)


DEFAULT_TEMPERATURE = float(
    os.getenv(
        "DEFAULT_TEMPERATURE",
        "0.7"
    )
)


DEFAULT_MAX_TOKENS = int(
    os.getenv(
        "DEFAULT_MAX_TOKENS",
        "1024"
    )
)



# Database
DATABASE_PATH = BASE_DIR / os.getenv(
    "DATABASE_PATH",
    "database/chatbot.db"
)
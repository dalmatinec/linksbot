
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get token from environment variables or use the hardcoded value as fallback
TOKEN = os.getenv("TELEGRAM_TOKEN", "7809435173:AAEdlLnntZqQLt_wxwdJ3gBCjASmcmp0ZFU")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "-1002443189526"))  # ID твоего чата

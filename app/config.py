import os
from dotenv import load_dotenv

load_dotenv()

GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE")
GIGACHAT_MODEL = os.getenv("GIGACHAT_MODEL")

if not GIGACHAT_CREDENTIALS:
    raise ValueError("Missing GIGACHAT_CREDENTIALS in environment variables.")
if not GIGACHAT_SCOPE:
    raise ValueError("Missing GIGACHAT_SCOPE in environment variables.")
if not GIGACHAT_MODEL:
    raise ValueError("Missing GIGACHAT_MODEL in environment variables.")

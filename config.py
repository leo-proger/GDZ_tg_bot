import os

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get('BOT_TOKEN')

SUBJECTS: list[str] = ['английский']

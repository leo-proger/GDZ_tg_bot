import os

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get('BOT_TOKEN')

# Предмет -> Серия учебника -> Класс -> Авторы
BOOKS: list[str] = [
	'Английский Spotlight 10 Класс Эванс',
	]

HEADERS = {
	'User-Agent': 'Mozilla/5.0',
	}

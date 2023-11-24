import os

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get('BOT_TOKEN')

# Со страницами или другой вид выбора задания -> Предмет -> Серия (Серия, Класс, Авторы)
SUBJECTS: dict = {
	'with_pages': {
		'Английский': ['Spotlight 10 Класс Эванс', ]
		}
	}

HEADERS = {
	'User-Agent': 'Mozilla/5.0',
	}

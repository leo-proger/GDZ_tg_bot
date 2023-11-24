import os

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get('BOT_TOKEN')

# Предмет, тип (учебник, рабочая тетрадь и тд), класс, авторы
SUBJECTS: dict[str: dict[str: str]] = {
	'with_pages':
		{
			'english': 'Английский Spotlight 10 класс Эванс',
			}
	}

HEADERS = {
	'User-Agent': 'Mozilla/5.0',
	}

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get('BOT_TOKEN')

# Предмет -> Серия учебника -> Класс -> Авторы
BOOKS: dict[str: str] = {
	'английский': 'Английский Spotlight 10 Класс В. Эванс, Д. Дули',
	'русский': 'Русский 10-11 Класс А.И. Власенков, Л.М. Рыбченкова',
	'алгебра-задачник': 'Алгебра-Задачник 10-11 Класс А.Г. Мордкович, П. В. Семенов',
	# TODO: 'алгебра-учебник': '...'
	}

HEADERS: dict[str: str] = {
	'User-Agent': 'Mozilla/5.0',
	}

ERROR_MESSAGE_404 = '{} не найден{}'
ERROR_MESSAGE_500 = 'Ой, у меня ошибка. Прошу написать ему >>> [Leo Proger](https://t.me/Leo_Proger)'

GREETING_MESSAGE = 'Привет, ***{first_name} {last_name}***!\n\nЧтобы посмотреть доступные учебники введи /list'

SLEEP_TIME: int = 120

NUMBER_PATTERN = r'^([1-9]|[1-3][0-9]|4[0-9]|49)\.\d+$'

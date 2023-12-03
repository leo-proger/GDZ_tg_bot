import os

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get('BOT_TOKEN')

# Предмет -> Серия учебника -> Класс -> Авторы
BOOKS: dict[str: str] = {
	'Английский': 'Английский Spotlight 10 Класс В. Эванс, Д. Дули',
	'Русский': 'Русский 10-11 класс Власенков А.И., Рыбченкова Л.М.',
	}

HEADERS: dict[str: str] = {
	'User-Agent': 'Mozilla/5.0',
	}

ERROR_MESSAGE_404 = 'Страница/Упражнение не найдено'
ERROR_MESSAGE_500 = 'Ой, у меня ошибка. Прошу написать ему >>> [Leo Proger](https://t.me/Leo_Proger)'

GREETING_MESSAGE = 'Привет, ***{first_name} {last_name}***!\n\nЧтобы посмотреть доступные учебники введи /list'

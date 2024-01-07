import asyncio
import re

from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import URLInputFile, Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app import config
from app.database import Users
from main import bot


async def send_solution(message: Message, result: dict[str: str], dialog_manager: DialogManager):
	if not result:
		# Обработка случая, когда решение не найдено
		await message.answer('Не найдено 😕')
	else:
		# Извлечение решения и заголовка из результата
		solution, title = result.get('solution'), result.get('title')
		if isinstance(solution, str):
			# Если решение представляет собой текст, разбиваем и отправляем его
			await send_split_text(message, solution)
		elif isinstance(solution, list):
			# Если решение - список URL-адресов, отправляем их соответственно
			await send_solution_urls(message, solution, title)
		await message.answer(title)
	await dialog_manager.done()


async def send_split_text(message: Message, solution: str):
	for text in split_text(solution):
		await message.answer(text)
		await asyncio.sleep(config.MESSAGE_DELAY)


async def send_solution_urls(message: Message, solution: list[str], title: str):
	for url in solution:
		if url.startswith('https://'):
			# Если URL - изображение, отправляем его как фото
			image = URLInputFile(url, filename=title)
			await bot.send_photo(chat_id=message.chat.id, photo=image)
		else:
			# Если это аннотация, то отправляем текст
			await message.answer(url)
		await asyncio.sleep(config.MESSAGE_DELAY)


def split_text(text: str, max_length: int = 4096) -> list[str]:
	# Находим границы предложений и абзацев
	boundaries = list(re.finditer(r'(?<=[.!?])\s+|\n', text))

	# Добавляем начало и конец текста в границы
	boundaries = [(-1, 0)] + [(m.start(), m.end()) for m in boundaries] + [(len(text), len(text))]

	# Объединяем предложения и абзацы, пока они не достигнут максимальной длины
	parts = []
	start = 0
	for i in range(1, len(boundaries)):
		if boundaries[i][0] - start > max_length:
			parts.append(text[start:boundaries[i - 1][1]])
			start = boundaries[i - 1][1]
	parts.append(text[start:])
	return parts


def get_annotation_text(book: str = None, **kwargs) -> str:
	base_text = f'Это все, что мне удалось найти по запросу:\n\nУчебник: ***{book}***\n' if book else ''
	additional_info = '\n'.join(
		[f'{key.capitalize()}: ***{value}***' for key, value in kwargs.items()]) if kwargs else ''
	return base_text + additional_info


async def send_whats_new(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
	users = await Users.get_users()

	message = '''
	Привет! Я обновился до версии ***2.0.0***

	***Что нового:***
	• Добавлены разделы для учебников
	• Добавлен новый учебник - физика
	• Теперь каждое обновление я буду оповещать вас о нем (если вам это не нравится, то прошу написать владельцу)
	• Исправлены ошибки
	'''
	for user in users:
		try:
			await bot.send_message(user, message)
		# await asyncio.sleep(100)
		except TelegramForbiddenError:
			print(f'Бот заблокирован пользователем {user}')
	await dialog_manager.done()

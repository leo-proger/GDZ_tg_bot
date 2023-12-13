import asyncio
import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile, ReplyKeyboardRemove

import config
from keyboards.keyboards import book_selection_kb
from main import bot
from parser import get_solve

router = Router()


class Form(StatesGroup):
	book = State()  # Отдельный учебник какого-то автора, серия

	page = State()  # Страница учебника
	exercise = State()  # Упражнение в учебнике
	number = State()  # Номер задания
	paragraph = State()  # Параграф учебника


@router.message(Command('list'))
async def book_selection(message: Message, state: FSMContext) -> None:
	await state.set_state(Form.book)

	await message.answer('Выбери учебник 📐📓📊📘', reply_markup=book_selection_kb())


@router.message(Form.book)
async def page_or_exercise_selection(message: Message, state: FSMContext) -> None:
	if message.text == config.BOOKS.get('русский'):
		await state.update_data(book=message.text)
		await state.set_state(Form.exercise)

		await message.answer('Теперь введи упражнение 📃 _(от 1 до 396 включительно)_',
		                     reply_markup=ReplyKeyboardRemove())

	elif message.text == config.BOOKS.get('английский'):
		await state.update_data(book=message.text)
		await state.set_state(Form.page)

		await message.answer('Теперь введи страницу 📖 _(от 10 до 180 включительно)_',
		                     reply_markup=ReplyKeyboardRemove())

	elif message.text == config.BOOKS.get('алгебра-задачник'):
		await state.update_data(book=message.text)
		await state.set_state(Form.number)

		await message.answer('Теперь введи номер задания 📖 _(от 1.1 до 60.19 включительно)_',
		                     reply_markup=ReplyKeyboardRemove())

	elif message.text == config.BOOKS.get('геометрия'):
		await state.update_data(book=message.text)
		await state.set_state(Form.number)

		await message.answer('Теперь введи номер задания 📖 _(от 1 до 870 включительно)_',
		                     reply_markup=ReplyKeyboardRemove())
	elif message.text == config.BOOKS.get('обществознание'):
		await state.update_data(book=message.text)
		await state.set_state(Form.paragraph)

		await message.answer('Теперь введи параграф учебника 📖 _(от 1 до 44 включительно)_\n\n'
		                     'Если у вас параграф вида _"число-число"_, то просто введите число перед дефисом',
		                     reply_markup=ReplyKeyboardRemove())
	else:
		await message.reply('Такого учебника, у меня нет 😕')
		await state.clear()


# Получить решение для учебников с выбором упражнения
@router.message(Form.exercise)
async def get_solve_exercise(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'exercise', 'Такого упражнения у меня нет 😕')


# Получить решение для учебников с выбором страницы
@router.message(Form.page)
async def get_solve_page(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'page', 'Такой страницы у меня нет 😕')


# Получить решение для учебников с выбором номера
@router.message(Form.number)
async def get_solve_number(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'number', 'Такого номера у меня нет 😕')


@router.message(Form.paragraph)
async def get_solve_number(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'paragraph', 'Такого параграфа у меня нет 😕')


async def get_solve_data(message: Message, state: FSMContext, data_key: str, error_message: str) -> None:
	if message.text.isdigit() or message.text.replace('.', '', 1).isdigit():
		await state.update_data({data_key: message.text})

		# book, page or exercise or number
		data: dict = await state.get_data()

		# Список url фото с решениями
		result = await get_solve(**data)
		status_code = result.get('status_code', 500)

		if status_code == 200:
			title = result.get('title')
			solution = result.get('solution')

			await send_solve(message=message, solution=solution, title=title)
		elif status_code == 404:
			text, suffix = result.get('text'), result.get('suffix')
			await message.answer(config.ERROR_MESSAGE_404.format(text, suffix))
		elif status_code == 500:
			await message.answer(config.ERROR_MESSAGE_500)
	else:
		await message.reply(error_message)
	await state.clear()


async def send_solve(message: Message, solution: list[str] | str, title: str) -> None:
	if isinstance(solution, str):
		for text in split_text(solution):
			await message.answer(text)
	else:
		for url in solution:
			image = URLInputFile(url, filename=title)
			await bot.send_photo(chat_id=message.chat.id, photo=image)

			# Задержка после отправки, чтобы телеграм не выдавал ошибку
			await asyncio.sleep(config.MESSAGE_DELAY)

		await message.answer(title)


def split_text(text: str, max_length: int = 4096):
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

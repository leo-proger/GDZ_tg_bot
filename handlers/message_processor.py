from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile, ReplyKeyboardRemove

import config
from keyboards.school_choice import book_selection_kb
from main import bot
from parser import get_solve

router = Router()


# TODO: Изменить название данного файла
class Form(StatesGroup):
	book = State()  # Отдельный учебник какого-то автора, серия
	page = State()  # Страница учебника
	exercise = State()  # Упражнение в учебнике


@router.message(Command('list'))
async def book_selection(message: Message, state: FSMContext) -> None:
	await state.set_state(Form.book)

	await message.answer('Выбери учебник 📐📓📊📘', reply_markup=book_selection_kb())


@router.message(Form.book)
async def page_or_exercise_selection(message: Message, state: FSMContext) -> None:
	if message.text == config.BOOKS.get('Русский'):
		await state.update_data(book=message.text)
		await state.set_state(Form.exercise)

		await message.answer('Теперь введи упражнение 📃', reply_markup=ReplyKeyboardRemove())

	elif message.text == config.BOOKS.get('Английский'):
		await state.update_data(book=message.text)
		await state.set_state(Form.page)

		await message.answer('Теперь введи страницу 📖', reply_markup=ReplyKeyboardRemove())
	else:
		await message.reply('Такого учебника, у меня нет 😕')


async def send_solve(message: Message, solutions_url: list[str], title: str) -> None:
	for url in solutions_url:
		image = URLInputFile(url, filename=title)
		await bot.send_photo(chat_id=message.chat.id, photo=image)

	await message.answer(title, parse_mode='Markdown')


async def get_solve_data(message: Message, state: FSMContext, data_key: str, error_message: str) -> None:
	if message.text.isdigit():
		await state.update_data({data_key: message.text})
		data: dict = await state.get_data()

		# Список url фото с решениями и название файла
		result = get_solve(*data.values())
		status_code = result.get('status_code', 500)

		if status_code == 200:
			title = result.get('title')
			solutions_url = result.get('solutions_url')

			await send_solve(message=message, solutions_url=solutions_url, title=title)
		elif status_code == 404:
			await message.answer(config.ERROR_MESSAGE_404)
		elif status_code == 500:
			await message.answer(config.ERROR_MESSAGE_500, parse_mode='MARKDOWN')
	else:
		await message.reply(error_message)
	await state.clear()


@router.message(Form.exercise)
async def get_solve_exercise(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'exercise', 'Такого упражнения у меня нет 😕')


@router.message(Form.page)
async def get_solve_page(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'page', 'Такой страницы у меня нет 😕')

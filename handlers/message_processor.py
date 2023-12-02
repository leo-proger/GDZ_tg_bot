from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile, ReplyKeyboardRemove

from config import BOOKS
from keyboards.school_choice import select_book_kb
from main import bot
from parser import get_solve

router = Router()


class Form(StatesGroup):
	book = State()  # Отдельный учебник какого-то автора, серия
	page = State()  # Страница учебника


@router.message(Command('start'))
async def greeting_and_select_book(message: Message, state: FSMContext) -> None:
	await state.set_state(Form.book)

	await message.answer(f'Привет, {message.from_user.first_name}')

	kb = select_book_kb()

	await message.answer('Выбери учебник 📐📓📊📘', reply_markup=kb)


@router.message(Form.book)
async def select_page(message: Message, state: FSMContext) -> None:
	if message.text in BOOKS:
		await state.update_data(book=message.text)
		await state.set_state(Form.page)

		await message.answer('Теперь введи страницу 📃', reply_markup=ReplyKeyboardRemove())
	else:
		await message.reply('Такого учебника, у меня нет 😕')


@router.message(Form.page)
async def get_exercise_solve(message: Message, state: FSMContext) -> None:
	if message.text.isdigit():
		await state.update_data(page=message.text)
		data: dict = await state.get_data()

		# Список url фото с решениями и название файла
		result = get_solve(*data.values())
		status_code = result.get('status_code', 500)

		if status_code == 200:
			title = result.get('title')

			for url in result.get('solutions_url'):
				image = URLInputFile(url, filename=title)
				await bot.send_photo(chat_id=message.chat.id, photo=image)

			await message.answer(title)
		elif status_code == 404:
			await message.answer('Страница не найдена')
		elif status_code == 500:
			await message.answer(
				'Ой, у меня ошибка. Прошу написать ему >>> [Leo Proger](https://t.me/Leo_Proger)',
				parse_mode='MARKDOWN')
	else:
		await message.reply('Такой страницы не существует')

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from app import config
from app.keyboards.keyboards import book_selection_kb
from ..utils import get_subject_text, check_numbering, send_solution, Parser

router = Router()


class FormBook(StatesGroup):
	book = State()  # Отдельный учебник какого-то автора
	numbering = State()  # Каким образом идет нумерация учебника (параграф, страница, номер задания)


@router.message(Command('list'))
async def book_selection(message: Message, state: FSMContext) -> None:
	await state.set_state(FormBook.book)

	await message.answer('Выбери учебник 📐📓📊📘', reply_markup=book_selection_kb())


@router.message(FormBook.book)
async def numbering_selection(message: Message, state: FSMContext) -> None:
	if message.text in config.BOOKS.values():
		await state.update_data(book=message.text)
		await state.set_state(FormBook.numbering)

		subject_text = get_subject_text(message.text)
		await message.answer(subject_text, reply_markup=ReplyKeyboardRemove())
	else:
		await message.reply('Такого учебника, у меня нет 😕')
		await state.clear()


@router.message(FormBook.numbering)
async def get_solve(message: Message, state: FSMContext) -> None:
	if check_numbering(message.text):
		await state.update_data(numbering=message.text)
		data = await state.get_data()

		book = data.get('book', '')
		numbering = data.get('numbering', '')

		parser = Parser(book, numbering)
		result = await parser.get_solution_data()

		if result:
			solution = result.get('solution')
			title = result.get('title')

			await send_solution(message, solution, title)
			await state.clear()
		else:
			await message.answer('Не найдено 😕')
	else:
		await message.answer('Не найдено 😕')

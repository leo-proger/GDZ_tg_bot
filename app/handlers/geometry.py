from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from ..keyboards.keyboards import GeometryKeyboards, book_selection_kb
from ..parsers import ParseGeometry
from ..utils import send_solution


router_geometry = Router()
geometry_kb = GeometryKeyboards()


class FormGeometry(StatesGroup):
	number = State()
	chapter_question = State()
	page = State()
	exercise_to_page = State()
	math_number = State()
	research_number = State()


@router_geometry.message(FormGeometry.exercise_to_page)
async def parse_exercise_to_page(message: Message, state: FSMContext) -> None:
	if message.text.isnumeric():
		await state.update_data(exercise_to_page=message.text)

		data = await state.get_data()
		page = data.get('page')

		parser = ParseGeometry(page=page, exercise_to_page=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()


@router_geometry.callback_query(F.data.startswith('geometry_page-'))
async def page_selection(callback: CallbackQuery, state: FSMContext) -> None:
	page = callback.data.split('-')[1]
	await state.update_data(page=page)
	await state.set_state(FormGeometry.exercise_to_page)

	await callback.message.edit_text('Осталось только ввести задачу', reply_markup=None)
	await callback.answer()


@router_geometry.callback_query(F.data.startswith('geometry_chapter-'))
async def parse_chapter(callback: CallbackQuery, state: FSMContext) -> None:
	await state.update_data(chapter_question=callback.data)
	chapter = callback.data.split('-')[1]

	parser = ParseGeometry(chapter=chapter)
	result = await parser.get_solution_data()

	await send_solution(callback.message, result, state)
	await callback.answer()


@router_geometry.callback_query(F.data.startswith('geometry_section-'))
async def section_selection(callback: CallbackQuery, state: FSMContext) -> None:
	section = callback.data.split('-')[1]

	if section == 'Номера':
		await state.set_state(FormGeometry.number)
		await callback.message.edit_text('Теперь введи номер _(от 1 до 870 включительно)_', reply_markup=None)
	elif section == 'Вопросы к главе':
		await state.set_state(FormGeometry.chapter_question)
		await callback.message.edit_text('Осталось выбрать главу',
		                                 reply_markup=geometry_kb.chapter_selection_kb())
	elif section == 'Задачи для подготовки ЕГЭ':
		await state.set_state(FormGeometry.page)
		await callback.message.edit_text('Теперь выбери страницу, где задачи для подготовки ЕГЭ',
		                                 reply_markup=geometry_kb.page_selection_kb())
	elif section == 'Задачи с мат. содержанием':
		await state.set_state(FormGeometry.math_number)
		await callback.message.edit_text('Введи задачу с математическим содержанием', reply_markup=None)
	elif section == 'Исследоват. задачи':
		await state.set_state(FormGeometry.research_number)
		await callback.message.edit_text('Введи номер исследовательской задачи', reply_markup=None)
	await callback.answer()


@router_geometry.message(FormGeometry.number)
async def parse_number(message: Message, state: FSMContext) -> None:
	if message.text.isnumeric():
		await state.update_data(number=message.text)

		parser = ParseGeometry(number=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()


@router_geometry.message(FormGeometry.math_number)
async def parse_math_number(message: Message, state: FSMContext) -> None:
	if message.text.isnumeric():
		await state.update_data(math_number=message.text)

		parser = ParseGeometry(math_number=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()


@router_geometry.message(FormGeometry.research_number)
async def parse_research_number(message: Message, state: FSMContext) -> None:
	if message.text.isnumeric():
		await state.update_data(research_number=message.text)

		parser = ParseGeometry(research_number=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()

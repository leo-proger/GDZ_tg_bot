import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from app import config
from app.keyboards.keyboards import PhysicsKeyboards, book_selection_kb
from app.parsers import ParsePhysics
from app.utils import send_solution

router_physics = Router()

kb_physics = PhysicsKeyboards()


class FormPhysics(StatesGroup):
	book = State()
	paragraph = State()
	question = State()
	exercise = State()


@router_physics.callback_query(F.data.startswith('physics_section-'))
async def section_selection(callback: CallbackQuery, state: FSMContext) -> None:
	section = callback.data.split('-')[1]

	if section == 'Вопросы':
		await state.set_state(FormPhysics.question)
		await callback.message.edit_text(
			'Теперь введи номер вопроса',
			reply_markup=None)
	elif section == 'Образцы заданий ЕГЭ':
		await state.set_state(FormPhysics.exercise)
		await callback.message.edit_text(
			'Теперь введи номер задания',
			reply_markup=None)
	await callback.answer()


@router_physics.message(FormPhysics.question)
async def parse_question(message: Message, state: FSMContext) -> None:
	if message.text.isnumeric():
		await state.update_data(question=message.text)
		data = await state.get_data()
		paragraph = data.get('paragraph')

		parser = ParsePhysics(paragraph=paragraph, question=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()


@router_physics.message(FormPhysics.exercise)
async def parse_question(message: Message, state: FSMContext) -> None:
	if message.text.isnumeric():
		await state.update_data(exercise=message.text)
		data = await state.get_data()
		paragraph = data.get('paragraph')

		parser = ParsePhysics(paragraph=paragraph, exercise=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()


@router_physics.message(FormPhysics.paragraph)
async def parse_question(message: Message, state: FSMContext) -> None:
	if message.text.isnumeric():
		await state.update_data(paragraph=message.text)
		data = await state.get_data()
		book = data.get('book')

		await message.answer('Теперь выбери раздел', reply_markup=kb_physics.section_selection_kb(book))
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()

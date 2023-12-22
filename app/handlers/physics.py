import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from app import config
from app.keyboards.keyboards import PhysicsKeyboards, book_selection_kb
from app.utils import send_solution, ParsePhysics

router_physics = Router()

kb_physics = PhysicsKeyboards()


class FormPhysics(StatesGroup):
	question = State()
	exercise = State()


@router_physics.callback_query(F.data.startswith('physics_section-'))
async def section_selection(callback: CallbackQuery, state: FSMContext) -> None:
	section = callback.data.split('-')[1]

	if section == 'Вопросы после параграфа':
		await state.set_state(FormPhysics.question)
		await callback.message.edit_text(
			'Теперь введи _параграф.номер вопроса_. Пример: Параграф - 9, Вопрос - 2. Значит вы вводите: _9.2_',
			reply_markup=None)
	elif section == 'Упражнения':
		await state.set_state(FormPhysics.exercise)
		await callback.message.edit_text(
			'Теперь введи _номер упражнения.номер задания_. Пример: Номер упражнения - 4, Номер задания - 1. '
			'Значит вы вводите: _4.1_',
			reply_markup=None)
	await callback.answer()


@router_physics.message(FormPhysics.question)
async def parse_question(message: Message, state: FSMContext) -> None:
	if re.match(config.FLOAT_NUMBER_PATTERN, message.text):
		await state.update_data(question=message.text)

		parser = ParsePhysics(question=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()


@router_physics.message(FormPhysics.exercise)
async def parse_question(message: Message, state: FSMContext) -> None:
	if re.match(config.FLOAT_NUMBER_PATTERN, message.text):
		await state.update_data(exercise=message.text)

		parser = ParsePhysics(exercise=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()

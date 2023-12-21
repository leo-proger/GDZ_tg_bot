from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from ..utils import ParseRussian, send_solution

router_russian = Router()


class FormRussian(StatesGroup):
	exercise = State()


@router_russian.message(FormRussian.exercise)
async def exercise_selection(message: Message, state: FSMContext):
	if message.text.isnumeric():
		await state.update_data(exercise=message.text)

		parser = ParseRussian(message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)

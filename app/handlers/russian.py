from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..parsers import ParseRussian
from ..states import FormRussian
from ..utils import send_solution

router_russian = Router()


@router_russian.message(FormRussian.exercise)
async def parse_exercise(message: Message, state: FSMContext):
	if message.text.isnumeric():
		await state.update_data(exercise=message.text)

		parser = ParseRussian(exercise=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)

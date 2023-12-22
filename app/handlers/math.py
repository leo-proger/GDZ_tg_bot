import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app import config
from app.keyboards.keyboards import book_selection_kb
from app.utils import send_solution, ParseMath

router_math = Router()


class FormMath(StatesGroup):
	number = State()


@router_math.message(FormMath.number)
async def parse_number(message: Message, state: FSMContext) -> None:
	if re.match(config.FLOAT_NUMBER_PATTERN, message.text):
		await state.update_data(number=message.text)

		parser = ParseMath(number=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()

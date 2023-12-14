from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.utils import get_solve_data

router = Router()


class FormNumber(StatesGroup):
	number = State()  # Номер задания


# Получить решение для учебников с выбором номера задания
@router.message(FormNumber.number)
async def get_solve_number(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'number', 'Такого номера у меня нет 😕')

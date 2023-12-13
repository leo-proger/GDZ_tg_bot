from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from app.utils import get_solve_data

router = Router()


class FormExercise(StatesGroup):
	exercise = State()  # Упражнение в учебнике


# Получить решение для учебников с выбором упражнения
@router.message(FormExercise.exercise)
async def get_solve_exercise(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'exercise', 'Такого упражнения у меня нет 😕')

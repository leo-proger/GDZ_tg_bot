from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.utils import get_solve_data

router = Router()


class FormParagraph(StatesGroup):
	paragraph = State()  # Параграф учебника


# Получить решение для учебников с выбором параграфа
@router.message(FormParagraph.paragraph)
async def get_solve_number(message: Message, state: FSMContext) -> None:
	await get_solve_data(message, state, 'paragraph', 'Такого параграфа у меня нет 😕')

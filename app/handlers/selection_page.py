from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.utils import get_solve_data

router = Router()


class FormPage(StatesGroup):
    page = State()  # Страница учебника


# Получить решение для учебников с выбором страницы
@router.message(FormPage.page)
async def get_solve_page(message: Message, state: FSMContext) -> None:
    await get_solve_data(message, state, 'page', 'Такой страницы у меня нет 😕')

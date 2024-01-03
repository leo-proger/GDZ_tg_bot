from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..keyboards.keyboards import book_selection_kb
from ..parsers import ParseSociology
from ..states import FormSociology
from ..utils import send_solution

router_sociology = Router()


@router_sociology.message(FormSociology.paragraph)
async def parse_paragraph(message: Message, state: FSMContext):
	if message.text.isnumeric():
		await state.update_data(parapgraph=message.text)

		parser = ParseSociology(paragraph=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()

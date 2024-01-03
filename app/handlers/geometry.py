from typing import Any

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.input import MessageInput

from ..parsers import ParseGeometry
from ..utils import send_solution


async def parse_chapter(callback: ChatEvent, select: Any, dialog_manager: DialogManager, item_id: str) -> None:
	dialog_manager.dialog_data['chapter'] = item_id

	parser = ParseGeometry(chapter=item_id)
	result = await parser.get_solution_data()

	await send_solution(callback.message, result, dialog_manager)


async def parse_exam_preparation_exercise(message: Message, message_input: MessageInput,
                                          dialog_manager: DialogManager) -> None:
	dialog_manager.dialog_data['exam_preparation_exercise'] = message.text

	page_for_exam_preparation_exercises = dialog_manager.dialog_data['page_for_exam_preparation_exercises']

	parser = ParseGeometry(page_for_exam_preparation_exercises=page_for_exam_preparation_exercises,
	                       exam_preparation_exercise=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)


async def parse_math_exercise(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
	dialog_manager.dialog_data['math_exercise'] = message.text

	parser = ParseGeometry(math_exercise=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)


async def parse_research_exercise(callback: ChatEvent, select: Any, dialog_manager: DialogManager,
                                  item_id: str) -> None:
	dialog_manager.dialog_data['research_exercise'] = item_id

	parser = ParseGeometry(research_exercise=item_id)
	result = await parser.get_solution_data()

	await send_solution(callback.message, result, dialog_manager)


async def geometry_parse_number(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
	dialog_manager.dialog_data['number'] = message.text

	parser = ParseGeometry(number=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)

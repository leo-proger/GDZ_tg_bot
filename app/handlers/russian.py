from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from ..parsers import ParseRussian
from ..utils import send_solution


async def russian_parse_exercise(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
	dialog_manager.dialog_data['exercise'] = message.text

	parser = ParseRussian(exercise=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)

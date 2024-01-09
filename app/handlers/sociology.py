from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from ..parsers import ParseSociology
from ..utils import send_solution


async def parse_paragraph(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
	dialog_manager.dialog_data['paragraph'] = message.text

	parser = ParseSociology(paragraph=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)

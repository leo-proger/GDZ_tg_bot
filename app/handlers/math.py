from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from app.parsers import ParseMath
from app.utils import send_solution


async def parse_number(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
	dialog_manager.dialog_data['number'] = message.text

	parser = ParseMath(number=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)

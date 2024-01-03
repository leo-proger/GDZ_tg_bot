from aiogram import Router
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from app.keyboards.keyboards import PhysicsKeyboards
from app.parsers import ParsePhysics
from app.utils import send_solution

router_physics = Router()

kb_physics = PhysicsKeyboards()


async def parse_question(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
	dialog_manager.dialog_data['question'] = message.text
	paragraph = dialog_manager.dialog_data['paragraph']

	parser = ParsePhysics(paragraph=paragraph, question=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)


async def physics_parse_exercise(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
	dialog_manager.dialog_data['exercise'] = message.text
	paragraph = dialog_manager.dialog_data['paragraph']

	parser = ParsePhysics(paragraph=paragraph, exercise=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)

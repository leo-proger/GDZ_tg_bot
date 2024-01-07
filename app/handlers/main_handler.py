from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..dialogs import *
from ..states import MainForm

router = Router()


# router.include_routers(
# 	main_dialog,
# 	dialog_admin,
#
# 	dialog_english,
# 	dialog_russian,
# 	dialog_math,
# 	dialog_geometry,
# 	dialog_sociology,
# 	dialog_physics
# 	)


@router.message(Command('start'))
async def greeting(message: Message) -> None:
	await message.answer(config.GREETING_MESSAGE.format(first_name=(message.from_user.first_name or ''),
	                                                    last_name=(message.from_user.last_name or ''))
	                     )


@router.message(Command('list'))
async def book_selection(message: Message, dialog_manager: DialogManager) -> None:
	await dialog_manager.start(MainForm.book)


@router.message(Command('help'))
async def get_help(message: Message) -> None:
	await message.answer(config.GET_HELP_MESSAGE)


@router.message(Command('admin'))
async def admin(message: Message, dialog_manager: DialogManager) -> None:
	if str(message.from_user.id) == '1491267583':
		await dialog_manager.start(AdminForm.admin)
	else:
		await message.answer('Чтобы отобразить список учебников, введите /list')


@router.message()
async def other(message: Message, state: FSMContext) -> None:
	await state.clear()
	await message.answer('Чтобы отобразить список учебников, введите /list')

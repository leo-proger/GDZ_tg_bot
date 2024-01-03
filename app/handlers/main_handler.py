from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from ..dialogs import *
from ..dialogs import main_dialog
from ..keyboards.keyboards import EnglishKeyboards, GeometryKeyboards, PhysicsKeyboards
from ..states import MainForm

router = Router()
router.include_routers(
	main_dialog,

	dialog_english,
	dialog_russian,
	dialog_math,
	dialog_geometry,
	dialog_sociology,
	# router_physics,
	)

english_kb = EnglishKeyboards()
geometry_kb = GeometryKeyboards()
physics_kb = PhysicsKeyboards()


@router.message(Command('list'))
async def book_selection(message: Message, dialog_manager: DialogManager) -> None:
	await dialog_manager.start(MainForm.book)

# @router.message(MainForm.book)
# async def subject_selection(message: Message, state: FSMContext) -> None:
# 	subject = message.text.split(' ', 1)[0].lower()
# 	if subject in config.BOOKS.keys():
# 		await state.update_data(book=message.text)
# 	# manager.dialog_data['book'] = message.text
# 	else:
# 		await message.reply('Не найдено 😕', reply_markup=ReplyKeyboardRemove())
# 		await state.clear()
# 	# await manager.done()
#
# 	if subject == 'английский':
# 		# await manager.start(FormEnglish.section)
# 		await message.answer('Теперь выбери раздел учебника',
# 		                     reply_markup=english_kb.section_selection_kb(message.text))

# elif subject == 'русский':
# 	await state.set_state(FormRussian.exercise)
#
# 	await message.answer('Теперь введи упражнение 📃 _(от 1 до 396 включительно)_',
# 	                     reply_markup=ReplyKeyboardRemove())
# elif subject == 'алгебра-задачник':
# 	await state.set_state(FormMath.number)
#
# 	await message.answer('Теперь введи номер задания 📖 _(от 1.1 до 60.19 включительно)_',
# 	                     reply_markup=ReplyKeyboardRemove())
# elif subject == 'геометрия':
# 	await message.answer('Теперь выбери раздел учебника',
# 	                     reply_markup=geometry_kb.section_selection_kb(message.text))
# elif subject == 'обществознание':
# 	await state.set_state(FormSociology.paragraph)
# 	await message.answer(
# 		'Теперь введи параграф учебника 📖 _(от 1 до 44 включительно)_\n\nЕсли у вас параграф вида '
# 		'_"число-число"_, то просто введите число перед дефисом',
# 		reply_markup=ReplyKeyboardRemove())
# elif subject == 'физика':
# 	await state.set_state(FormPhysics.book)
# 	await state.update_data(book=message.text)
# 	await state.set_state(FormPhysics.paragraph)
#
# 	await message.answer('Теперь введи параграф', reply_markup=ReplyKeyboardRemove())

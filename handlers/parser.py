from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import config
import utils
from keyboards.choice_gdz import choice_subject_kb

router = Router()
validator = utils.Validator(subjects=config.SUBJECTS)


class Form(StatesGroup):
	subject = State()


@router.message(Command('start'))
async def greeting_and_choice_subject(message: Message, state: FSMContext):
	await state.set_state(Form.subject)
	await message.answer(f'Привет, {message.from_user.first_name}')

	kb = choice_subject_kb()

	await message.answer('Выбери предмет:', reply_markup=kb)


@router.message(Form.subject)
async def choice_page(message: Message, state: FSMContext):
	if validator.validate_subject(message.text.lower()):
		await state.update_data(subject=message.text.lower())
		print('alright')
	else:
		await message.reply('Такого предмета нет')

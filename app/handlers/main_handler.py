from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from app import config
from app.keyboards.keyboards import book_selection_kb
from . import selection_exercise
from . import selection_number
from . import selection_page
from . import selection_paragraph

router = Router()
router.include_routers(
    selection_page.router,
    selection_exercise.router,
    selection_number.router,
    selection_paragraph.router,
)


class FormBook(StatesGroup):
    book = State()  # Отдельный учебник какого-то автора


@router.message(Command('list'))
async def book_selection(message: Message, state: FSMContext) -> None:
    await state.set_state(FormBook.book)

    await message.answer('Выбери учебник 📐📓📊📘', reply_markup=book_selection_kb())


@router.message(FormBook.book)
async def page_or_exercise_selection(message: Message, state: FSMContext) -> None:
    if message.text == config.BOOKS.get('русский'):
        await state.update_data(book=message.text)
        await state.set_state(selection_exercise.FormExercise.exercise)

        await message.answer('Теперь введи упражнение 📃 _(от 1 до 396 включительно)_',
                             reply_markup=ReplyKeyboardRemove())

    elif message.text == config.BOOKS.get('английский'):
        await state.update_data(book=message.text)
        await state.set_state(selection_page.FormPage.page)

        await message.answer('Теперь введи страницу 📖 _(от 10 до 180 включительно)_',
                             reply_markup=ReplyKeyboardRemove())

    elif message.text == config.BOOKS.get('алгебра-задачник'):
        await state.update_data(book=message.text)
        await state.set_state(selection_number.FormNumber.number)

        await message.answer('Теперь введи номер задания 📖 _(от 1.1 до 60.19 включительно)_',
                             reply_markup=ReplyKeyboardRemove())

    elif message.text == config.BOOKS.get('геометрия'):
        await state.update_data(book=message.text)
        await state.set_state(selection_number.FormNumber.number)

        await message.answer('Теперь введи номер задания 📖 _(от 1 до 870 включительно)_',
                             reply_markup=ReplyKeyboardRemove())
    elif message.text == config.BOOKS.get('обществознание'):
        await state.update_data(book=message.text)
        await state.set_state(selection_paragraph.FormParagraph.paragraph)

        await message.answer('Теперь введи параграф учебника 📖 _(от 1 до 44 включительно)_\n\n'
                             'Если у вас параграф вида _"число-число"_, то просто введите число перед дефисом',
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply('Такого учебника, у меня нет 😕', reply_markup=ReplyKeyboardRemove())
        await state.clear()

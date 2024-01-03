from aiogram.fsm.state import StatesGroup, State


# main_handler.py
class MainForm(StatesGroup):
	book = State()  # Отдельный учебник какого-то автора


# english.py
class FormEnglish(StatesGroup):
	section = State()
	page = State()
	spotlight_on_russia_page = State()
	module = State()
	module_exercise = State()


# geometry.py
class FormGeometry(StatesGroup):
	number = State()
	chapter_question = State()
	page = State()
	exercise_to_page = State()
	math_number = State()
	research_number = State()


# math.py
class FormMath(StatesGroup):
	number = State()


# physics.py
class FormPhysics(StatesGroup):
	book = State()
	paragraph = State()
	question = State()
	exercise = State()


# russian.py
class FormRussian(StatesGroup):
	exercise = State()


# sociology.py
class FormSociology(StatesGroup):
	paragraph = State()

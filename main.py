import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from app.config import TOKEN
from app.handlers import main_handler, default_handlers
from app.middlewares.add_user_to_db_middleware import AddUserToDatabaseMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode='Markdown')


async def main():
	dp = Dispatcher(storage=MemoryStorage())

	main_handler.router.message.middleware(AddUserToDatabaseMiddleware())
	default_handlers.router.message.middleware(AddUserToDatabaseMiddleware())

	dp.include_routers(
		main_handler.router,
		default_handlers.router,
		)
	setup_dialogs(dp)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	print('Бот работает...')
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Бот закончил работу.')

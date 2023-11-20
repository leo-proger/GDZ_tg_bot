import asyncio

from aiogram import Bot, Dispatcher

import config
from handlers import parser

bot = Bot(token=config.TOKEN, parse_mode='html')


async def main():
	dp = Dispatcher()

	dp.include_router(parser.router)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	print('Бот работает...')
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Бот закончил работу.')

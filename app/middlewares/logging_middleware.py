import logging
import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.config import SLEEP_TIME


class LoggingMiddleware(BaseMiddleware):
	def __init__(self):
		self.users = {}

	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: Dict[str, Any],
			) -> Any:
		user = data['event_from_user']
		user_id = user.id

		if user_id not in self.users:
			self.users[user_id] = time.time()
		else:
			if time.time() - self.users[user_id] < SLEEP_TIME:
				return await handler(event, data)
			else:
				self.users[user_id] = time.time()

		username = (user.first_name or '') + ' ' + (user.last_name or '')
		logging.info(f'User: {username}, {user_id}')

		result = await handler(event, data)
		return result

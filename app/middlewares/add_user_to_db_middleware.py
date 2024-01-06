import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database import Users


class AddUserToDatabaseMiddleware(BaseMiddleware):
	async def __call__(
			self,
			handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
			event: TelegramObject,
			data: Dict[str, Any],
			**kwargs,
			) -> Any:
		user = data['event_from_user']

		user_id = user.id
		first_name_short = fn[:10] + '...' if (fn := user.first_name) and len(fn) > 10 else fn
		last_name_short = ln[:10] + '...' if (ln := user.last_name) and len(ln) > 10 else ln

		adding_user = await Users.add_user(user_id, user.first_name, user.last_name)
		status_code: int = adding_user.get('status_code')

		if status_code == 200:
			logging.info(f'Пользователь {first_name_short} {last_name_short} {user_id} успешно добавлен в Базу Данных')
		return await handler(event, data)

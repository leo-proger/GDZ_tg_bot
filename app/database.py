import aiomysql

from .config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class User:
	def __init__(self, telegram_id: int, first_name: str = None, last_name: str = None) -> None:
		self.telegram_id = telegram_id
		self.first_name = first_name
		self.last_name = last_name

	async def add_user(self) -> dict[str: int]:
		pool = await aiomysql.create_pool(
			host=MYSQL_HOST,
			user=MYSQL_USER,
			password=MYSQL_PASSWORD,
			db=MYSQL_DATABASE
			)

		async with pool.acquire() as conn:
			async with conn.cursor() as cur:
				# Проверка наличия пользователя в базе данных
				await cur.execute('SELECT * FROM Users WHERE telegram_id = %s', (self.telegram_id,))
				user = await cur.fetchone()

				# Если пользователь не найден, добавляем его в базу данных
				if user is None:
					await cur.execute('INSERT INTO Users (telegram_id, first_name, last_name) VALUES (%s, %s, %s)',
					                  (self.telegram_id, self.first_name, self.last_name))
					await conn.commit()
					return {'status_code': 200}
				return {'status_code': 409}

	@staticmethod
	async def get_users() -> list[list]:
		pool = await aiomysql.create_pool(
			host=MYSQL_HOST,
			user=MYSQL_USER,
			password=MYSQL_PASSWORD,
			db=MYSQL_DATABASE
			)
		async with pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute("SELECT telegram_id, first_name, last_name FROM Users")

				users = []
				async for row in cur:
					users.append([row[0], row[1], row[2]])
		return users

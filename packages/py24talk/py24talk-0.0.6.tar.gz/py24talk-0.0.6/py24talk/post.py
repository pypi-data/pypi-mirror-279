from .content import Content
from .exceptions import NotFoundError, UnknownError

class Post(Content):
	"""
	Пост.
	"""
	
	def __init__(self, post_id):
		"""
		Аргументы:
			post_id (int): Идентификатор поста.
		"""
		self._post_id = post_id
	
	async def __get_post(self):
		response = await self.get_content(f"posts/{self._post_id}.json")

		if "error_type" in response:
			if response["error_type"] == "not_found":
				raise NotFoundError("Не удалось найти пост.", "Проверьте корректность идентификатора поста.")
			else:
				raise UnknownError(response["error_type"])

		return response
	
	async def author(self):
		"""Автор поста."""
		from .user import User
		return User((await self.__get_post())["username"])
	
	async def content(self):
		"""Контент поста."""
		return (await self.__get_post())["raw"]
	
	async def created(self):
		"""Дата и время создания поста."""
		return (await self.__get_post())["created_at"]
	
	async def is_wiki(self):
		"""Является ли пост вики-постом."""
		return (await self.__get_post())["wiki"]
	
	async def likes(self):
		"""Кол-во лайков под постом."""
		check = (await self.__get_post()).get("actions_summary")

		if check:
			for tmp in check:
				if tmp["id"] == 2:
					return tmp["count"]
		
		return 0

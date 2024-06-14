from .content import Content

class Post(Content):
	"""
	Пост.
	"""
	
	def __init__(self, post_id: str) -> None:
		"""
		Аргументы:
			post_id (int): Идентификатор поста.
		"""
		self._post_id = post_id
	
	async def __get_post(self) -> dict:
		return await self.get_content(f"posts/{self._post_id}.json")
	
	async def author(self) -> User:
		"""Автор поста."""
		from .user import User
		return User((await self.__get_post())["username"])
	
	async def content(self) -> str:
		"""Контент поста."""
		return (await self.__get_post())["raw"]
	
	async def created(self) -> str:
		"""Дата и время создания поста."""
		return (await self.__get_post())["created_at"]
	
	async def is_wiki(self) -> bool:
		"""Является ли пост вики-постом."""
		return (await self.__get_post())["wiki"]
	
	async def likes(self) -> int:
		"""Кол-во лайков под постом."""
		check = (await self.__get_post()).get("actions_summary")

		if check:
			for tmp in check:
				if tmp["id"] == 2:
					return tmp["count"]
		
		return 0

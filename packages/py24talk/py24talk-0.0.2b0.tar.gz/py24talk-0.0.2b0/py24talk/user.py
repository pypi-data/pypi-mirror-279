from .content import Content
from typing import Optional

class User(Content):
	"""
	Пользователь.
	"""

	def __init__(self, username: str) -> None:
		"""
		Аргументы:
			username (str): Никнейм пользователя.
		"""
		self._usename = username

	async def __get_user(self) -> dict:
		return await self.get_content("u/" + self._username + ".json")

	async def username(self) -> str:
		"""Ник пользователя."""
		return (await self.__get_user())["user"]["username"]

	async def name(self) -> Optional[str]:
		"""Имя пользователя."""
		name = (await self.__get_user())["user"]["name"]
		return name if len(name) != 0 else None

	async def avatar(self, size: int = 400) -> str:
		"""
		Ссылка на аватарку пользователя.

		Аргументы:
			size (int): Разрешение аватарки.
		"""
		return self.endpoint[:-1] + (await self.__get_user())["user"]["avatar_template"].format(size = size)

	async def bio(self) -> Optional[str]:
		"""Описание пользователя."""
		return (await self.__get_user())["user"].get("bio_raw")

	async def website(self) -> Optional[str]:
		"""Сайт пользователя."""
		return (await self.__get_user())["user"].get("website")

	async def location(self) -> Optional[str]:
		"""Местоположение пользователя."""
		return (await self.__get_user())["user"].get("location")

	async def title(self) -> Optional[str]:
		"""Титул (статус) пользователя."""
		title = (await self.__get_user())["user"].get("title")
		return title if len(title) != 0 else None

	async def trust_level(self) -> int:
		"""
		Уровень доверия пользователя.
		1 - Обычный пользователь.
		2 - Участник.
		3 - Активный пользователь.
		4 - Лидер.
		"""
		return (await self.__get_user())["user"]["trust_level"]

	async def badges(self) -> list:
		"""Полный список достижений пользователя."""
		badges = (await self.get_content("user-badges/" + self._username + ".json"))["badges"]
		from .badge import Badge
		return [Badge(badge_data) for badge_data in badges]

	async def pinned_badges(self) -> list:
		"""Достижения которые находятся в карточке пользователя."""
		badges = (await self.__get_user())["badges"]
		return [Badge(badge_data) for badge_data in badges]

	async def is_banned(self) -> bool:
		"""Забанен ли пользователь (мип)?"""
		return (await self.__get_user())["user"].get("suspend_reason") is not None

	async def invited_by(self) -> Optional["User"]:
		"""Пользователь, который пригласил данного пользователя."""
		check = (await self.__get_user())["user"].get("invited_by")

		if not check:
			return None
		
		return User(check.get("username"))

	async def card_background(self) -> Optional[str]:
		"""Ссылку на фон карточки пользователя."""
		path = (await self.__get_user())["user"].get("card_background_upload_url")

		if not path:
			return None
		
		return self.endpoint[:-1] + path

	async def profile_background(self) -> Optional[str]:
		"""Возвращает ссылку на фон профиля пользователя."""
		path = (await self.__get_user())["user"].get("profile_background_upload_url")

		if not path:
			return None
		
		return self.endpoint[:-1] + path

	async def featured_topic(self) -> Optional[Topic]:
		"""Избранный топик пользователя."""
		topic = (await self.__get_user())["user"].get("featured_topic")

		if not topic:
			return None

		from .topic import Topic
		return Topic(topic["id"])
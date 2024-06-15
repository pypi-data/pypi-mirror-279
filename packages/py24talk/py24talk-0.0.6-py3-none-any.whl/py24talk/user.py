from .content import Content
from typing import Optional
from .exceptions import NotFoundError, UnknownError

class User(Content):
	"""
	Пользователь.
	"""

	def __init__(self, username):
		"""
		Аргументы:
			username (str): Никнейм пользователя.
		"""
		self._username = username

	async def __get_user(self):
		response = await self.get_content("u/" + self._username + ".json")

		if "error_type" in response:
			if response["error_type"] == "not_found":
				raise NotFoundError("Не удалось найти пользователя.", "Проверьте корректность ника пользователя.")
			else:
				raise UnknownError(response["error_type"])
		
		return response

	async def username(self):
		"""Ник пользователя."""
		return (await self.__get_user())["user"]["username"]

	async def name(self):
		"""Имя пользователя."""
		name = (await self.__get_user())["user"]["name"]
		return name if len(name) != 0 else None

	async def avatar(self, size=400):
		"""
		Ссылка на аватарку пользователя.

		Аргументы:
			size (int): Разрешение аватарки.
		"""
		return self.endpoint[:-1] + (await self.__get_user())["user"]["avatar_template"].format(size=size)

	async def bio(self):
		"""Описание пользователя."""
		return (await self.__get_user())["user"].get("bio_raw")

	async def website(self):
		"""Сайт пользователя."""
		return (await self.__get_user())["user"].get("website")

	async def location(self):
		"""Местоположение пользователя."""
		return (await self.__get_user())["user"].get("location")

	async def title(self):
		"""Титул (статус) пользователя."""
		title = (await self.__get_user())["user"].get("title")
		return title if len(title) != 0 else None

	async def trust_level(self):
		"""
		Уровень доверия пользователя.
		1 - Обычный пользователь.
		2 - Участник.
		3 - Активный пользователь.
		4 - Лидер.
		"""
		return (await self.__get_user())["user"]["trust_level"]

	async def badges(self):
		"""Полный список достижений пользователя."""
		badges = (await self.get_content("user-badges/" + self._username + ".json"))["badges"]

		if "error_type" in badges:
			if badges["error_type"] == "not_found":
				raise NotFoundError("Не удалось найти пост.", "Проверьте корректность идентификатора поста.")
			else:
				raise UnknownError(badges["error_type"])
			
		from .badge import Badge
		return [Badge(badge_data) for badge_data in badges]

	async def pinned_badges(self):
		"""Достижения которые находятся в карточке пользователя."""
		badges = (await self.__get_user())["badges"]
		from .badge import Badge
		return [Badge(badge_data) for badge_data in badges]

	async def is_banned(self):
		"""Забанен ли пользователь (мип)?"""
		return (await self.__get_user())["user"].get("suspend_reason") is not None

	async def invited_by(self):
		"""Пользователь, который пригласил данного пользователя."""
		check = (await self.__get_user())["user"].get("invited_by")

		if not check:
			return None
		
		return User(check.get("username"))

	async def card_background(self):
		"""Ссылку на фон карточки пользователя."""
		path = (await self.__get_user())["user"].get("card_background_upload_url")

		if not path:
			return None
		
		return self.endpoint[:-1] + path

	async def profile_background(self):
		"""Возвращает ссылку на фон профиля пользователя."""
		path = (await self.__get_user())["user"].get("profile_background_upload_url")

		if not path:
			return None
		
		return self.endpoint[:-1] + path

	async def featured_topic(self):
		"""Избранный топик пользователя."""
		topic = (await self.__get_user())["user"].get("featured_topic")

		if not topic:
			return None

		from .topic import Topic
		return Topic(topic["id"])

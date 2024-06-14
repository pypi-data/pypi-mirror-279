from .content import Content

class Badge(Content):
	"""Достижение."""

	def __init__(self, badge_data: dict) -> None:
		"""
		Аргументы:
			badge_data (dict): Данные достижения.
		"""
		self.data = badge_data
	
	async def name(self) -> str:
		"""Название достижения."""
		return self.data["name"]
	
	async def description(self, in_html: bool) -> str:
		"""
		Описание достижения.

		Аргументы:
			in_html (bool): В виде HTML.
		"""
		description = self.data["description"]
		return description if in_html else await self.remove_html_tags(description)
	
	async def having_count(self) -> int:
		"""Кол-во пользователей имеющих данное достижения."""
		return self.data["grant_count"]
	
	async def preciousness(self) -> int:
		"""
		Ценность достижения.
		1 - Золотой.
		2 - Серебренный.
		3 - Бронзовый.
		"""
		return self.data["badge_type_id"]
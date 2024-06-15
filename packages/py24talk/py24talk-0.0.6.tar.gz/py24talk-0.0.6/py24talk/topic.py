from .post import Post
from asyncio import sleep
from .exceptions import NotFoundError, UnknownError

class Topic(Post):
	"""
	Топик (тема).
	"""
	
	def __init__(self, topic_id):
		"""
		Аргументы:
			topic_id (int): Идентификатор топика.
		"""
		self._topic_id = topic_id
	
	async def get_post(self, postion):
		"""
		Получить пост (ответ) под топиком.
		Если 1 (int) то сам топик.

		Аргументы:
			position (int): Позиция поста.
		"""
		post_id = None

		try:
			page = 1

			while True:
				response = (await self.get_content(f"t/{self._topic_id}.json?page={page}"))["post_stream"]["posts"]

				if (
					response[-1]["post_number"] >= postion and
					response[0]["post_number"] <= postion
				):
					for post in response:
						
						if post["post_number"] == postion:
							post_id = post["id"]
							break

					break

				page += 1
				await sleep(0.5) # 2 запроса в секунду. Ограничение форума.
		except KeyError:
			pass

		if not post_id:
			return None
		
		return Post(post_id)
from asyncio import sleep

class Topic(Post):
	"""
	Топик (тема).
	"""
	
	def __init__(self, topic_id: int) -> None:
		"""
		Аргументы:
			topic_id (int): Идентификатор топика.
		"""
		self._topic_id = topic_id
	
	async def get_post(self, postion: int) -> Post:
		"""
		Получить пост (ответ) под топиком.

		Аргументы:
			position (int): Позиция поста.
		"""
		post_id = None

		try:
			page = 1

			while True:
				check = (await self.get_content(f"t/{self._topic_id}.json?page={page}"))["post_stream"]["posts"]
				if (
					check[-1]["post_number"] >= postion and
					check[0]["post_number"] <= postion
				):
					for post in check:
						
						if post["post_number"] == postion:
							post_id = post["id"]
							break

					break

				page += 1
				await sleep(0.5)
		except KeyError:
			pass

		if not post_id:
			return None
		
		from .post import Post
		return Post(post_id)
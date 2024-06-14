from .managers.requests import get_json

class Content:

	endpoint = "https://talk.24serv.pro/"

	async def get_content(self, path: str) -> dict:
		return await get_json(self.endpoint + path)
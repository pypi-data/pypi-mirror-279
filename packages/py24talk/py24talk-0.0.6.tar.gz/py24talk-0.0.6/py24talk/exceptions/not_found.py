class NotFoundError(Exception):

	def __init__(self, message: str, fix_answer: str) -> None:
		super().__init__(message)
		self.fix_answer = fix_answer

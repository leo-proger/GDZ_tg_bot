class Validator:
	def __init__(self, subjects: list[str]) -> None:
		self.subjects = subjects

	def validate_subject(self, subject: str) -> bool:
		return True if subject.isalpha() and subject in self.subjects else False

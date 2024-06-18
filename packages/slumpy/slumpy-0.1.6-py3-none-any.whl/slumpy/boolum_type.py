class Boolum ():
	
	def __init__ (self, entry : bool = False) -> None:

		self._element : bool = entry

	def set_to (self, entry : bool = False) -> bool:

		self._element = entry
		return (self._element)

	def value (self) -> bool:

		return (self._element)

	def opposite (self) -> bool:

		return (not self._element)

	def switch (self) -> bool:

		self._element = not self._element
		return (self._element)

	def to_string (self) -> str:

		return (f"Boolum : {self._element}")

class Boolumpy (Boolum):

	def __repr__ (self) -> str:

		return (str (self._element))

	def __not__ (self) -> bool:

		return (not self._element)

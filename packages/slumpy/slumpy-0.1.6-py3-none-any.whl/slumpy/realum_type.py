class Realum ():
	
	def __init__ (self, entry : float = 0.0) -> None:

		self._element : float = entry

	def set_to (self, entry : float = 0.0) -> float:

		self._element = entry
		return (self._element)

	def value (self) -> float:

		return (self._element)

	def plus (self, entry : float = 0.0) -> float:

		return (self._element + entry)

	def minus (self, entry : float = 0.0) -> float:

		return (self._element - entry)

	def multiplied_by (self, entry : float = 1.0) -> float:

		return (self._element * entry)

	def divided_by (self, entry : float = 1.0) -> float:

		return (self._element / entry)

	def power_of (self, entry : float = 1.0) -> float:

		return (self._element ** entry)

	def set_plus (self, entry : float = 0.0) -> float:

		self._element += entry
		return (self._element)

	def set_minus (self, entry : float = 0.0) -> float:

		self._element -= entry
		return (self._element)

	def set_multiplied_by (self, entry : float = 1.0) -> float:

		self._element *= entry
		return (self._element)

	def set_divided_by (self, entry : float = 1.0) -> float:

		self._element /= entry
		return (self._element)
	
	def set_power_of (self, entry : float = 1.0) -> float:

		self._element **= entry
		return (self._element)

	def is_equal_to (self, entry : float = 0.0) -> bool:

		return (self._element == entry)

	def is_not_equal_to (self, entry : float = 0.0) -> bool:

		return (self._element != entry)

	def is_greater_than (self, entry : float = 0.0) -> bool:

		return (self._element > entry)

	def is_less_than (self, entry : float = 0.0) -> bool:

		return (self._element < entry)

	def is_greater_than_or_equal_to (self, entry : float = 0.0) -> bool:

		return (self._element >= entry)

	def is_less_or_equal_than (self, entry : float = 0.0) -> bool:

		return (self._element <= entry)

	def to_string (self) -> str:

		return (f"Realum : {self._element}")

class Realumpy (Realum):

	def __repr__ (self) -> str:

		return (str (self._element))

	def __add__ (self, entry : float = 0.0) -> float:

		return (self._element + entry)

	def __sub__ (self, entry : float = 0.0) -> float:

		return (self._element - entry)

	def __mul__ (self, entry : float = 1.0) -> float:

		return (self._element * entry)

	def __truediv__ (self, entry : float = 1.0) -> float:

		return (self._element / entry)

	def __floordiv__ (self, entry : float = 1.0) -> float:

		return (self._element // entry)

	def __pow__ (self, entry : float = 1.0) -> float:

		return (self._element ** entry)
	
	def __iplus__ (self, entry : float = 0.0) -> float:

		return (self._element + entry)

	def __isub__ (self, entry : float = 0.0) -> float:

		return (self._element - entry)

	def __imul__ (self, entry : float = 1.0) -> float:

		return (self._element * entry)

	def __itruediv__ (self, entry : float = 1.0) -> float:

		return (self._element / entry)

	def __ifloordiv__ (self, entry : float = 1.0) -> float:

		return (self._element // entry)

	def __ipow__ (self, entry : float = 1.0) -> float:

		return (self._element ** entry)

	def __eq__ (self, entry : float = 0.0) -> bool:

		return (self._element == entry)

	def __ne__ (self, entry : float = 0.0) -> bool:

		return (self._element != entry)

	def __gt__ (self, entry : float = 0.0) -> bool:

		return (self._element > entry)

	def __lt__ (self, entry : float = 0.0) -> bool:

		return (self._element < entry)

	def __ge__ (self, entry : float = 0.0) -> bool:

		return (self._element >= entry)

	def __le__ (self, entry : float = 0.0) -> bool:

		return (self._element <= entry)

	def __abs__ (self) -> int:

		return (abs (self._element))

	def __neg__ (self) -> int:

		return (-self._element)
	
	def __round__ (self) -> int:

		return (round (self._element))
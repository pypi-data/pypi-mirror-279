class Intum ():
	
	def __init__ (self, entry : int = 0) -> None:

		self._element : int = entry

	def set_to (self, entry : 0) -> int:

		self._element = entry
		return (self._element)

	def value (self) -> int:

		return (self._element)

	def plus (self, entry : int = 0) -> int:

		return (self._element + entry)

	def minus (self, entry : int = 0) -> int:

		return (self._element - entry)

	def multiplied_by (self, entry : int = 1) -> int:

		return (self._element * entry)

	def divided_by (self, entry : int = 1) -> int:

		return (self._element // entry)

	def power_of (self, entry : int = 1) -> int:

		return (self._element ** entry)

	def module_of (self, entry : int = 1) -> int:

		return (self._element % entry)

	def set_plus (self, entry : int = 0) -> int:

		self._element += entry
		return (self._element)

	def set_minus (self, entry : int = 0) -> int:

		self._element -= entry
		return (self._element)

	def set_multiplied_by (self, entry : int = 1) -> int:

		self._element *= entry
		return (self._element)

	def set_divided_by (self, entry : int = 1) -> int:

		self._element //= entry
		return (self._element)

	def set_power_of (self, entry : int = 1) -> int:

		self._element **= entry
		return (self._element)

	def set_module_of (self, entry : int = 1) -> int:

		self._element %= entry
		return (self._element)

	def is_equal_to (self, entry : int = 0) -> bool:

		return (self._element == entry)

	def is_not_equal_to (self, entry : int = 0) -> bool:

		return (self._element != entry)

	def is_greater_than (self, entry : int = 0) -> bool:

		return (self._element > entry)

	def is_less_than (self, entry : int = 0) -> bool:

		return (self._element < entry)

	def is_greater_than_or_equal_to (self, entry : int = 0) -> bool:

		return (self._element >= entry)

	def is_less_than_or_equal_to (self, entry : int = 0) -> bool:

		return (self._element <= entry)
	
	def to_string (self) -> str:

		return (f"Intum : {self._element}")

class Intumpy (Intum):

	def __repr__ (self) -> str:

		return (str (self._element))

	def __add__ (self, entry : int = 0) -> int:

		return (self._element + entry)

	def __sub__ (self, entry : int = 0) -> int:

		return (self._element - entry)

	def __mul__ (self, entry : int = 1) -> int:

		return (self._element * entry)

	def __truediv__ (self, entry : int = 1) -> int:

		return (self._element // entry)

	def __floordiv__ (self, entry : int = 1) -> int:

		return (self._element // entry)

	def __mod__ (self, entry : int = 1) -> int:

		return (self._element % entry)

	def __pow__ (self, entry : int = 1) -> int:

		return (self._element ** entry)

	def __iadd__ (self, entry : int = 0) -> int:

		self._element += entry
		return (self._element)

	def __isub__ (self, entry : int = 0) -> int:

		self._element -= entry
		return (self._element)

	def __imul__ (self, entry : int = 1) -> int:

		self._element *= entry
		return (self._element)

	def __itruediv__ (self, entry : int = 1) -> int:

		self._element //= entry
		return (self._element)

	def __ifloordiv__ (self, entry : int = 1) -> int:

		self._element //= entry
		return (self._element)

	def __imod__ (self, entry : int = 1) -> int:

		self._element %= entry
		return (self._element)

	def __ipow__ (self, entry : int = 1) -> int:

		self._element **= entry
		return (self._element)

	def __eq__ (self, entry : int = 0) -> bool:

		return (self._element == entry)

	def __ne__ (self, entry : int = 0) -> bool:

		return (self._element != entry)

	def __gt__ (self, entry : int = 0) -> bool:

		return (self._element > entry)

	def __lt__ (self, entry : int = 0) -> bool:

		return (self._element < entry)

	def __ge__ (self, entry : int = 0) -> bool:

		return (self._element >= entry)

	def __le__ (self, entry : int = 0) -> bool:

		return (self._element <= entry)

	def __abs__ (self) -> int:

		return (abs (self._element))

	def __neg__ (self) -> int:

		return (-self._element)
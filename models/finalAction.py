import enum
from functools import total_ordering

# @total_ordering
class FinalAction(enum.Enum):
	
	HOLD = "HOLD"
	BUY = "BUY"
	SELL = "SELL"
	
	
	# def __eq__(self, other):
	# 	if self.__class__ is other.__class__:
	# 		return self.value == other.value
	# 		return NotImplemented
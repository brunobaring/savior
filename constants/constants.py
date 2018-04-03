import enum


class GuessConstant(enum.Enum):
	
	HOLD = "HOLD"
	BUY = "BUY"
	SELL = "SELL"
	NULL = "NULL"
	

	def objectFor(value):
		for i in list(GuessConstant):
			if i.value == value:
				return i
		print("Unknown GuessConstant. Quitting..")
		exit()
class Guess:

	constant = None
	weight = 0

	def __init__(self, guessConstant, weight, strategy):
		self.strategy = strategy
		self.constant = guessConstant
		self.weight = weight
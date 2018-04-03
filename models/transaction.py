from constants.constants import GuessConstant

class Transaction:

	guesses = None
	candle = None
	
	def __init__(self, guess, stoploss = 100):
		self.guesses = []
		self.guesses.append(guess)
		self.stoploss = stoploss

	def action(self):

		guessConstants = list(GuessConstant)
		sums = {}

		for guess in self.guesses:
			for guessConstant in guessConstants:
				if guess.constant == guessConstant:
					if guess.constant in sums:
						sums[guess.constant.value] += guess.weight
					else:
						sums[guess.constant.value] = guess.weight
		sums.pop(GuessConstant.HOLD.value, None)
		sums.pop(GuessConstant.NULL.value, None)

		highestWeight = 0
		highestGuess = None

		for guess, weight in sums.items():
			if weight > highestWeight:
				highestWeight = weight
				highestGuess = guess
			elif weight == highestWeight:
				print("caso louco!!! deu empate entre duas decisões: " + guess + " e " + highestGuess + ". Tratar essa excessão. Por isso, o programa será encerrado")
				exit()

		if highestGuess == None:
			return GuessConstant.HOLD
		return GuessConstant.objectFor(highestGuess)

	def addPossibilities(self, guess):
		self.guesses.append(guess)

	@staticmethod
	def rentability(initialPrice, finalPrice, fees):
		return (finalPrice / initialPrice - 1) * 100 * (1 - fees) #percent
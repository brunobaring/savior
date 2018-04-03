from constants.constants import GuessConstant
from models.guess import Guess

class StopLossStrategy:

	def __init__(self, stopLoss, rentability):
		self.stopLoss = stopLoss
		self.rentability = rentability

	def whatShouldYouDo(self):
		if self.rentability < -self.stopLoss:
			return Guess(GuessConstant.SELL, 10)
		else:
			return Guess(GuessConstant.HOLD, 1)
from constants.constants import GuessConstant
from models.guess import Guess

class ProfitTargetStrategy:

	def __init__(self, profitTarget, rentability):
		self.profitTarget = profitTarget
		self.rentability = rentability

	def whatShouldYouDo(self):
		if self.rentability >= self.profitTarget:
			return Guess(GuessConstant.SELL, 10)
		else:
			return Guess(GuessConstant.HOLD, 1)
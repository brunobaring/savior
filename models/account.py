from models.finalAction import FinalAction

class Account():
	criptoBalance = 0

	def __init__(self, criptoBalance):
		self.criptoBalance = criptoBalance

	def evaluateFinalAction(self, candle, finalAction, operationValue):
		if finalAction == FinalAction.BUY:
			self.criptoBalance += operationValue
		if finalAction == FinalAction.SELL:
			self.criptoBalance -= operationValue
		return self.fiatBalance(candle)

	def fiatBalance(self, candle):
		fiatBalance = candle.close * self.criptoBalance
		return str(fiatBalance)

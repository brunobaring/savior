from models.finalAction import FinalAction

class Account():
	baseBalance = 0
	quoteBalance = 0

	def __init__(self, quoteBalance):
		self.quoteBalance = quoteBalance
		self.initialBalance = quoteBalance

	def evaluateFinalAction(self, candle, finalAction, operationValue):
		if finalAction == FinalAction.BUY:
			self.baseBalance = self.quoteBalance / candle.close
			self.quoteBalance = 0
			return self.baseBalance
		if finalAction == FinalAction.SELL:
			self.quoteBalance = self.baseBalance * candle.close
			self.baseBalance = 0
			return self.quoteBalance
		

	def fiatBalance(self, candle):
		fiatBalance = candle.close * self.baseBalance
		return fiatBalance

from models.transaction import Transaction
from constants.constants import GuessConstant
from general import savPrint

class Account():

	baseBalance = 0
	quoteBalance = 0
	transaction = None
	lastTransaction = None

	def __init__(self, quoteBalance):
		self.quoteBalance = quoteBalance
		self.initialBalance = quoteBalance

	def evaluateTransaction(self, transaction):
		self.makeLastTransaction(transaction)
		action = self.transaction.action()

		if action == GuessConstant.BUY:
			self.baseBalance = self.quoteBalance / self.transaction.candle.close
			self.quoteBalance = 0
			self.transaction = transaction
			return self.baseBalance

		if action == GuessConstant.SELL:
			self.quoteBalance = self.baseBalance * self.transaction.candle.close
			self.baseBalance = 0
			self.transaction = transaction
			return self.quoteBalance
		
	def makeLastTransaction(self, transaction):
		self.lastTransaction = self.transaction
		self.transaction = transaction

	def rentability(self, value, fees):
		action = self.transaction.action()
		if action == GuessConstant.BUY:
			return "" # str(round(self.calculateRentability(value * self.baseBalance, 0), 2))
		elif action == GuessConstant.SELL:
			return str(round(self.calculateRentability(self.quoteBalance, 0), 2))


	def calculateRentability(self, finalPrice, fees):
		return (finalPrice / self.initialBalance - 1) * 100 * (1 - fees) #percent

	def printStatus(self, candleDate):
		rentability = ""
		if self.lastTransaction != None and self.transaction.action() == GuessConstant.SELL:
			rentability = str(Transaction.rentability(self.lastTransaction.candle.close, self.transaction.candle.close, 0))
			
		print(
			self.transaction.action().value +
			"\t->\t" +
			str(candleDate.year) + 
			"/" + 
			str(candleDate.month) + 
			"/" + 
			str(candleDate.day) + 
			" " + 
			str(candleDate.hour) + 
			":" + 
			str(candleDate.minute) + 
			":00\t- " + 
			self.finalBalanceCurrency() + 
			" " + 
			self.finalBalanceFormated() + 
			"\t" + 
			rentability
		)

	def printFinalBalance(self):
		savPrint(
			"Rentability = " + 
			self.rentability(self.transaction.candle.close, 0) + 
			" % "
		)
		
		savPrint("Final Balance = " + 
			self.finalBalanceCurrency() + 
			self.finalBalanceFormated()
		)

	def finalBalanceCurrency(self):
		action = self.transaction.action()
		if action == GuessConstant.BUY:
			return "BTC"
		elif action == GuessConstant.SELL:
			return "USDT"

	def finalBalanceFormated(self):
		action = self.transaction.action()		
		if action == GuessConstant.BUY:
			return str(round(self.baseBalance,8))
		elif action == GuessConstant.SELL:
			return str(round(self.quoteBalance,2))

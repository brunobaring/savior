from datetime import datetime
from general import toBinanceDateFormat, toEpoch, savPrint
from tests.testableData import TestableData
from strategies.exponentialMovingAverageStrategy import ExponentialMovingAverageStrategy
from models.account import Account
from models.transaction import Transaction
from models.candle import CandleFactory
from models.guess import Guess
from constants.constants import GuessConstant
from strategies.stopLossStrategy import StopLossStrategy

class TestSavior:
	
	startYear = 0
	startMonth = 0
	startDay = 0
	startHour = 0
	endYear = 0
	endMonth = 0
	endDay = 0
	endHour = 0
	interval = 0
	account = None

	def __init__(
		self,
		startYear = 2017,
		startMonth = 8,
		startDay = 17,
		startHour = 21,
		startMinute = 8,
		endYear = 2017,
		endMonth = 11,
		endDay = 9,
		endHour = 10,
		endMinute = 39,
		interval = 1,
		initialBalance = 1000, # Começa com 1000 USD
		limits = [8, 13, 21, 55],
		stopLoss = 0,
		profitTarget = 0

	):
		self.startYear = startYear
		self.startMonth = startMonth
		self.startDay = startDay
		self.startHour = startHour
		self.startMinute = startMinute
		self.endYear = endYear
		self.endMonth = endMonth
		self.endDay = endDay
		self.endHour = endHour
		self.endMinute = endMinute
		self.verifyDates()
		self.stopLoss = stopLoss
		self.profitTarget = profitTarget

		# self.interval = interval
		self.account = Account(initialBalance)
		self.limits = limits

	def start(self):
		savPrint("Savior Started.", 3)
		self.whatShouldYouDo()

		print("end")

	def whatShouldYouDo(self):
		candles = TestableData.jsonData()
		candles = CandleFactory.candlesWithJson(candles)
		fakeSellGuess = Guess(GuessConstant.SELL, 10)
		lastAction = GuessConstant.SELL
		lastCandle = None
		savPrint("Initial Balance = USDT " + str(self.account.quoteBalance))

		for i in range(self.limits[-1]*2+1, len(candles)):
			
			candle = candles[i]
			if float(candle.closeTime) < float(toBinanceDateFormat(datetime(self.startYear, self.startMonth, self.startDay, self.startHour, self.startMinute))):
				continue
			
			if str(candle.closeTime + 1) > (toBinanceDateFormat(datetime(self.endYear, self.endMonth, self.endDay, self.endHour, self.endMinute))):
				break

			candleDate = datetime.fromtimestamp(float(candle.closeTime)/1000)
			exponentialMovingAverageStrategy = ExponentialMovingAverageStrategy(
					interval = "1h",
					limits = self.limits,
					endYear = candleDate.year,
					endMonth = candleDate.month,
					endDay = candleDate.day,
					endHour = candleDate.hour,
					endMinute = candleDate.minute,
					shouldPrintMovingAverages = False,
					isTesting = True
				)

			exponentialMovingAverageGuess = exponentialMovingAverageStrategy.whatShouldYouDo()
			self.transaction = Transaction(exponentialMovingAverageGuess, self.stopLoss)

			if lastCandle != None and lastAction == GuessConstant.BUY:
				rentability = Transaction.rentability(lastCandle.close, candle.close,0)

				stopLossStrategy = StopLossStrategy(
						stopLoss = self.stopLoss,
						rentability = rentability
					)
				stopLossGuess = stopLossStrategy.whatShouldYouDo()
				self.transaction.addPossibilities(stopLossGuess)

				profitTargetStrategy = ProfitTargetStrategy(
						stopLoss = self.profitTarget,
						rentability = rentability
					)
				profitTargetGuess = profitTargetStrategy.whatShouldYouDo()
				self.transaction.addPossibilities(profitTargetGuess)


			action = self.transaction.action()
			self.transaction.candle = candle

			if action != GuessConstant.HOLD and action != lastAction:
				self.account.evaluateTransaction(self.transaction)
				lastAction = action
				self.account.printStatus(candleDate)
				lastCandle = candle

		savPrint("Reached end")
		self.account.printFinalBalance()


	def verifyDates(self):
		startDateTime = datetime(self.startYear, self.startMonth, self.startDay, self.startHour)
		startDate = toBinanceDateFormat(startDateTime)

		endDateTime = datetime(self.endYear, self.endMonth, self.endDay, self.endHour)
		endDate = toBinanceDateFormat(endDateTime)

		if self.doesInputDateExistAndMakesChronologicalSense(startDate, endDate):
			savPrint("Invalid input dates", 6)
			exit()

	def doesInputDateExistAndMakesChronologicalSense(self, startDate, endDate):
		candles = TestableData.jsonData()
		candles = CandleFactory.candlesWithJson(candles)
		prices = []

		startDateFound = False
		for candle in candles:
			if startDate == candle.closeTime:
				startDateFound = True

			if endDate == candle.closeTime:
				if startDateFound:
					return True
				else:
					return False
		return False

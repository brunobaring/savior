from datetime import datetime
from general import toBinanceDateFormat
from tests.testableData import TestableData
from general import savPrint
from strategies.exponentialMovingAverageStrategy import ExponentialMovingAverageStrategy
from models.account import Account
from models.finalAction import FinalAction
from models.candle import CandleFactory
from general import toEpoch

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
	operationsValue = 0

	def __init__(
		self,
		startYear = 2017,
		startMonth = 8,
		startDay = 17,
		startHour = 21,
		endYear = 2017,
		endMonth = 11,
		endDay = 9,
		endHour = 10,
		interval = 1,
		initialBalance = 1000, # Começa com 1000 USD
		operationsValue = 1, # Essa variável tá morta
		limits = [8, 13, 21, 55]
	):
		self.startYear = startYear
		self.startMonth = startMonth
		self.startDay = startDay
		self.startHour = startHour
		self.endYear = endYear
		self.endMonth = endMonth
		self.endDay = endDay
		self.endHour = endHour
		self.verifyDates()

		# self.interval = interval
		self.account = Account(initialBalance)
		self.operationsValue = operationsValue
		self.limits = limits
	def start(self):
		self.whatShouldYouDo()

	def whatShouldYouDo(self):
		savPrint("Savior Started.", 3)
		self.testExponentialMovingAverageStrategy()
		
		print("end")

	def testExponentialMovingAverageStrategy(self):
		candles = TestableData.jsonData()
		candles = CandleFactory.candlesWithJson(candles)
		lastFinalAction = FinalAction.SELL

		savPrint("Initial Balance = USDT " + str(self.account.quoteBalance))

		for i in range(self.limits[-1]*2+1, len(candles)):
			candle = candles[i]

			if float(candle.closeTime) < float(toBinanceDateFormat(datetime(self.startYear, self.startMonth, self.startDay, self.startHour))):
				continue

			if str(candle.closeTime + 1) > (toBinanceDateFormat(datetime(self.endYear, self.endMonth, self.endDay, self.endHour))):
				savPrint("Reached end")
				if lastFinalAction == FinalAction.BUY:
					savPrint("Final Balance = BTC " + str(self.account.baseBalance) + " = USDT " + str(self.account.fiatBalance(lastCandle)))
					savPrint("Rentability = " + str((self.account.fiatBalance(lastCandle)/self.account.initialBalance - 1)*100) + " % ")
				elif lastFinalAction == FinalAction.SELL:
					savPrint("Final Balance = USDT " + str(self.account.quoteBalance))
					savPrint("Rentability = " + str((self.account.quoteBalance/self.account.initialBalance - 1)*100) + " % ")
				return

			candleDate = datetime.fromtimestamp(float(candle.closeTime)/1000)
			exponentialMovingAverageStrategy = ExponentialMovingAverageStrategy(
					interval = 1,
					limits = self.limits,
					endYear = candleDate.year,
					endMonth = candleDate.month,
					endDay = candleDate.day,
					endHour = candleDate.hour,
					shouldPrintMovingAverages = False,
					isTesting = True
				)
			whatShouldYouDo, candle = exponentialMovingAverageStrategy.whatShouldYouDo()
			if not whatShouldYouDo == FinalAction.HOLD and lastFinalAction != whatShouldYouDo:
				lastFinalAction = whatShouldYouDo
				lastCandle = candle
				self.account.evaluateFinalAction(candle, whatShouldYouDo, self.operationsValue)
				if lastFinalAction == FinalAction.BUY:
					CURRENCY = " \t- BTC "
					BALANCE = self.account.baseBalance
				if lastFinalAction == FinalAction.SELL:
					CURRENCY = " \t- USDT "
					BALANCE = self.account.quoteBalance
				print(whatShouldYouDo.value + " \t->\t " + str(candleDate.year) + "/" + str(candleDate.month) + "/" + str(candleDate.day) + " " + str(candleDate.hour) + CURRENCY + str(BALANCE))


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

from datetime import datetime
from general import toBinanceDateFormat
from tests.testableData import TestableData
from general import savPrint
from strategies.exponentialMovingAverageStrategy import ExponentialMovingAverageStrategy
from models.account import Account
from models.finalAction import FinalAction
from models.candle import CandleFactory

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
		initialBalance = 2,
		operationsValue = 1
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
	def start(self):
		self.whatShouldYouDo()

	def whatShouldYouDo(self):
		savPrint("Savior Started.", 3)
		self.testExponentialMovingAverageStrategy()
		
		print("end")

	def testExponentialMovingAverageStrategy(self):
		candles = TestableData.jsonData()
		candles = CandleFactory.candlesWithJson(candles)
		lastFinalAction = None

		savPrint("Initial Balance = R$" + self.account.fiatBalance(candles[0]), 3)

		limits = [8, 13, 21, 55]
		for i in range(limits[-1]*2+1, len(candles)):
			candle = candles[i]
			if str(candle.openTime) == (toBinanceDateFormat(datetime(self.endYear, self.endMonth, self.endDay, self.endHour))):
				savPrint("Reached end")
				exit()
			candleDate = datetime.fromtimestamp(float(candle.openTime)/1000)
			exponentialMovingAverageStrategy = ExponentialMovingAverageStrategy(
					interval = 1,
					limits = limits,
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
				self.account.evaluateFinalAction(candle, whatShouldYouDo, self.operationsValue)
				print(whatShouldYouDo.value + " \t->\t " + str(candleDate.year) + "/" + str(candleDate.month) + "/" + str(candleDate.day) + " " + str(candleDate.hour) + " \t- R$ " + self.account.fiatBalance(candle))


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
			if startDate == candle.openTime:
				startDateFound = True

			if endDate == candle.openTime:
				if startDateFound:
					return True
				else:
					return False
		return False
from datetime import datetime
from general import toBinanceDateFormat
from tests.testableData import TestableData
from general import savPrint
from strategies.exponentialMovingAverageStrategy import ExponentialMovingAverageStrategy
from models.account import Account

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
		endYear = 2017,
		endMonth = 11,
		endDay = 9,
		endHour = 10,
		interval = 1,
		initialBalance = 1000
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

	def start(self):
		self.whatShouldYouDo()

	def whatShouldYouDo(self):
		savPrint("Savior Started.", 3)
		whatShouldYouDo, candle = self.testExponentialMovingAverageStrategy()
		
		self.account.evaluateBalance(candle, whatShouldYouDo)

		print("end")

	def testExponentialMovingAverageStrategy(self):
		candles = TestableData.jsonData()
		limits = [8, 13, 21, 55]
		for i in range(limits[-1]*2+1, len(candles)):
			candle = candles[i]
			if str(candle[0]) == (toBinanceDateFormat(datetime(self.endYear, self.endMonth, self.endDay, self.endHour))):
				savPrint("Reached endDate")
				exit()
			candleDate = datetime.fromtimestamp(float(candle[0])/1000)
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
			print(whatShouldYouDo.value + " -> " + str(candleDate.year) + "/" + str(candleDate.month) + "/" + str(candleDate.day) + " " + str(candleDate.hour))

		return whatShouldYouDo, candle


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
		prices = []

		startDateFound = False
		for candle in candles:
			if startDate == candle[0]:
				startDateFound = True

			if endDate == candle[0]:
				if startDateFound:
					return True
				else:
					print()
					return False
		return False
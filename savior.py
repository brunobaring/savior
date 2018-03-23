 # -*- coding: utf-8 -*-
import time
import datetime
import dateutil.parser
import urllib.request
import requests
from datetime import datetime, timedelta, date
from dateutil.parser import parse
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import pprint
from fulldata import allData
import json

class TestableData:

	@staticmethod
	def prices():
		candles = allData()
		prices = []
		for candle in candles:
			prices.append(candle[4])
		return prices

	def jsonData():
		return allData()



class TestSavior:
	
	prices = []
	startYear = 0
	startMonth = 0
	startDay = 0
	startHour = 0
	endYear = 0
	endMonth = 0
	endDay = 0
	endHour = 0
	interval = 0
	initialBalance = 0

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
		self.prices = TestableData.prices()

	def start(self):
		self.whatShouldYouDo()

	def whatShouldYouDo(self):
		savPrint("Savior Started.", 3)

		candles = TestableData.jsonData()
		for candle in candles:
			candleDate = datetime.fromtimestamp(float(candle[0])/1000)
			exponentialMovingAverageStrategy = ExponentialMovingAverageStrategy(
					interval = 1,
					limits = [8, 13, 21, 55],
					endYear = candleDate.year,
					endMonth = candleDate.month,
					endDay = candleDate.day,
					endHour = candleDate.hour,
					isTesting = True
				)

			whatShouldYouDo = exponentialMovingAverageStrategy.whatShouldYouDo()
			print(whatShouldYouDo + " -> " + str(candleDate.year) + "/" + str(candleDate.month) + "/" + str(candleDate.day) + " " + str(candleDate.hour))

		print("end")

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
					return False
		return False
class Savior:

####################### CONFIGURABLE #######################
	#SHOULD ACTIVATE SCHEDULER
	# timer que roda o bot de tanto em tanto tempo
	shouldActivateScheduler = False

	#SCHEDULER SECONDS
	# intervalo de tempo para rodar o bot, caso esteja ativado
	schedulerSeconds = 4
####################### CONFIGURABLE #######################

	def start(self):
		if self.shouldActivateScheduler:
			self.activateScheduler()
		else:
			self.whatShouldYouDo()

	def whatShouldYouDo(self):
		savPrint("Savior Started.", 3)
		exponentialMovingAverageStrategy = ExponentialMovingAverageStrategy()
		savPrint("YOU SHOULD " + exponentialMovingAverageStrategy.whatShouldYouDo() + "!!!", 4)

	def activateScheduler(self):
		savPrint("Ctrl + C para matar o Savior.")
		scheduler = BlockingScheduler()
		scheduler.add_job(self.whatShouldYouDo, 'interval', seconds=self.schedulerSeconds)
		scheduler.start()


class ExponentialMovingAverageStrategy:


####################### CONFIGURABLE #######################

	#PAIR
	# ETHETC, LTCUSDT, BTCETH, por aí vai, nesse formato, em caixa alta.
	symbol = ""

	#INTERVAL
	# intervalo de 12 horas. só pode ser 12, 8, 4, 2, 1. Por enquanto só pode horas aqui nesse programa. Rola de usar outros tempos.
	# m -> minutes; h -> hours; d -> days; w -> weeks; M -> months
	# 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
	interval = 0

	#LIMITS
	# escala exponencial das médias móveis
	limits = []

	#END TIME FORMAT
	# formato: YYYY-MM-dd I
	# a data final para o cálculo da média móvel.
	# a data inicial é calculada a partir do interval e o último limite da escala
	endYear = 0
	endMonth = 0
	endDay = 0
	endHour = 0

	#SHOULD PRINT PAYLOAD
	# exibe ou não o resultado da API
	shouldPrintPayload = None

	#SHOULD PRINT PAYLOAD
	# exibe ou não o resultado da API
	shouldPrintMovingAverages = None

####################### CONFIGURABLE #######################

	startTime = ""
	endTime = ""
	dataLimit = 0
	isTesting = None

	def __init__(
			self,
			symbol = "BTCUSDT",
			interval = 1,
			limits = [8, 13, 21, 55],
			endYear = 2018,
			endMonth = 2,
			endDay = 27,
			endHour = 9,
			shouldPrintPayload = False,
			shouldPrintMovingAverages = False,
			isTesting = False
		):

		self.symbol = symbol
		self.interval = interval
		self.limits = limits
		self.endYear = endYear
		self.endMonth = endMonth
		self.endDay = endDay
		self.endHour = endHour
		self.shouldPrintPayload = shouldPrintPayload
		self.shouldPrintMovingAverages = shouldPrintMovingAverages
		self.isTesting = isTesting

		self.dataLimit = self.limits[-1]*2+1

		# -> pega a data final
		endDate = datetime(self.endYear,self.endMonth,self.endDay,self.endHour)
		#   -> subtrai a quantidade de horas do intervalo vezes o último limite
		endDateWithSubtractedHours = endDate - timedelta(hours=self.interval*self.dataLimit)

		self.startTime = toBinanceDateFormat(endDateWithSubtractedHours)
		self.endTime = toBinanceDateFormat(endDate)

	def whatShouldYouDo(self):
		url = KlinesResource().urlFor(self)
		json = makeRequest(url, self.shouldPrintPayload, self.isTesting)
		candles = CandleFactory.candlesWithJson(json)

		movingAverage = []
		for limit in self.limits:
			movingAverage.append(self.ema(candles, limit))

		return self.evaluateMovingAverage(movingAverage)

	def ema(self, candles, n):
	    """
	    returns an n period exponential moving average for
	    the time series s

	    s is a list ordered from oldest (index 0) to most
	    recent (index -1)
	    n is an integer

	    returns a numeric array of the exponential
	    moving average
	    """

	    s = [] # array(s)
	    for candle in candles:
	    	s.append(candle.close)

	    ema = []
	    j = 1

	    #get n sma first and calculate the next n period ema
	    sma = sum(s[:n]) / n
	    multiplier = 2 / float(1 + n)
	    ema.append(sma)

	    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
	    ema.append(( (s[n] - sma) * multiplier) + sma)

	    #now calculate the rest of the values
	    for i in s[n+1:]:
	        tmp = ( (i - ema[j]) * multiplier) + ema[j]
	        j = j + 1
	        ema.append(tmp)

	    return ema


	def evaluateMovingAverage(self, movingAverages):

		if self.shouldPrintMovingAverages:
			savPrint("Printing Moving Averages...", 3)
			for i in range(len(movingAverages)):
				savPrint(str(i + 1) + "- " + str(movingAverages[i]))

		lastEma = movingAverages[-1]		

		isAtLeastOneEmaBelowInPreviousTendency = False
		for i, ema in enumerate(movingAverages):
			if lastEma[-2] - ema[-2] > 0:
				isAtLeastOneEmaBelowInPreviousTendency = True
			if lastEma[-1] - ema[-1] < 0:
				if i == len(movingAverages)-2 and isAtLeastOneEmaBelowInPreviousTendency:
					return "BUY"
			else:
				break

		isAtLeastOneEmaAboveInPreviousTendency = False
		for i, ema in enumerate(movingAverages):
			if lastEma[-2] - ema[-2] < 0:
				isAtLeastOneEmaAboveInPreviousTendency = True
			if lastEma[-1] - ema[-1] > 0:
				if i == len(movingAverages)-2 and isAtLeastOneEmaAboveInPreviousTendency:
					return "SELL"
			else:
				break

		return "HOLD"


class CandleFactory:

	@staticmethod
	def oneCandleWithJson(json):
		return Candle(json)

	@staticmethod
	def candlesWithJson(json):
		candles = []
		for jsonCandle in json:
			candle = CandleFactory.oneCandleWithJson(jsonCandle)
			candles.append(candle)
		return candles


class Candle:

	openTime = 0
	close = 0
	closeTime = 0

	def __init__(self, json):
		self.openTime = json[0]
		self.close = float(json[4])
		self.closeTime = json[6]



def makeRequest(url, shouldPrintPayload, isTesting = False):

	if isTesting:
		response = TestableData.jsonData()
		if shouldPrintPayload:
			pp = pprint.PrettyPrinter(indent=4)
			pp.pprint(response)
		return response

	else:
		savPrint("Making Request to URL " + url)

		r = requests.get(url)

		if r.status_code == 429 :
			savPrint("You should stop the script", 6)
		if r.status_code == 418:
			savPrint("You`ve been banned from Binance", 6)
			exit()

		response = r.json()

		if shouldPrintPayload:
			pp = pprint.PrettyPrinter(indent=4)
			pp.pprint(response)

		return response


def savPrint(string, indent = 1):
	indented = ""
	for i in range(indent):
		indented += ">"
	print(" -" + indented + " " + str(string) + "\n")

def toEpoch(date):
	return (date - datetime(1970,1,1)).total_seconds()

def toBinanceDateFormat(date):
	return str(int(toEpoch(date))).ljust(13, '0')

class Resources:

	baseApi = "https://api.binance.com/api"
	apiVersion = "/v1"
	endpoint = ""
	params = []

	def getUrl(self):
		return self.baseApi + self.apiVersion + self.endpoint + "?" + "&".join(self.params)

class KlinesResource(Resources):

	endpoint = "/klines"

	def urlFor(self, data):
		self.params = [
			"symbol=" + data.symbol,
			"interval=" + str(data.interval) + "h",
			"startTime=" + data.startTime,
			"endTime=" + data.endTime,
			"limit=" + str(data.dataLimit)
		]
		return self.getUrl()

# savior = Savior().start()
testSavior = TestSavior().start()
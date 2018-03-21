 # -*- coding: utf-8 -*-
from urllib.request import urlopen
import json
import time
import datetime
import dateutil.parser
import urllib.request

from datetime import datetime, timedelta, date
from dateutil.parser import parse
from datetime import datetime


class Savior:

	def start(self):

		savPrint("Savior Started.", 3)
		movingAverageStrategy = MovingAverageStrategy()
		savPrint("YOU SHOULD " + movingAverageStrategy.whatShouldYouDo() + "!!!", 4)




class MovingAverageStrategy:


####################### CONFIGURABLE #######################

	#PAIR
	# ETHETC, LTCUSDT, BTCETH, por aí vai, nesse formato, em caixa alta.
	symbol = "LTCUSDT"

	#INTERVAL
	# intervalo de 12 horas. só pode ser 12, 8, 4, 2, 1. Por enquanto só pode horas aqui nesse programa. Rola de usar outros tempos.
	# m -> minutes; h -> hours; d -> days; w -> weeks; M -> months
	# 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
	interval = 4

	#LIMITS
	# escala exponencial das médias móveis
	limits = [8, 13, 21, 55]

	#ENDTIMEFORMAT
	# formato: YYYY-MM-dd I
	# a data final para o cálculo da média móvel.
	# a data inicial é calculada a partir do interval e o último limite da escala
	endYear = 2018
	endMonth = 2
	endDay = 27
	endHour = 12

	#SHOULDPRINTPAYLOAD
	# exibe ou não o resultado da API
	shouldPrintPayload = False

	#SHOULDPRINTPAYLOAD
	# exibe ou não o resultado da API
	shouldPrintMovingAverages = True

####################### CONFIGURABLE #######################

	startTime = ""
	endTime = ""

	def __init__(self):

		# -> pega a data final
		endDate = datetime(self.endYear,self.endMonth,self.endDay,self.endHour)
		#   -> subtrai a quantidade de horas do intervalo vezes o último limite
		endDateWithSubtractedHours = endDate - timedelta(hours=self.interval*self.limits[-1]+1)

		self.startTime = str(int(toEpoch(endDateWithSubtractedHours))).ljust(13, '0')
		self.endTime = str(int(toEpoch(endDate))).ljust(13, '0')

	def whatShouldYouDo(self):
		url = self.prepareRequest()
		json = makeRequest(url, self.shouldPrintPayload)
		candles = self.parseToCandles(json)

		movingAverage = []
		for limit in self.limits:
			movingAverage.append(self.ema(candles, limit))

		return self.evaluateMovingAverage(movingAverage)

	def prepareRequest(self):

		savPrint("Preparing Request...")

		baseApi = "https://api.binance.com/api"
		apiVersion = "/v1"
		endpoint = "/klines"
		params = [
			"symbol=" + self.symbol,
			"interval=" + str(self.interval) + "h",
			"startTime=" + self.startTime,
			"endTime=" + self.endTime,
			"limit=" + str(self.limits[-1]+1)
		]
		url = baseApi + apiVersion + endpoint + "?" + "&".join(params)

		return url

	def parseToCandles(self, jsonCandles):
		candles = []
		for jsonCandle in jsonCandles:
			candle = Candle(jsonCandle)
			candles.append(candle)
		return candles

	# def calculateMovingAverageCandleQty(self, qty, candles):
	# 	candleCloseSummary = 0
	# 	for i in range(int(qty)-1):
	# 		candleCloseSummary += candles[i].close
	# 	return candleCloseSummary/float(qty)

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
	    print(str(len(candles)) + " " + str(n))
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
				if i == len(movingAverages)-1 and isAtLeastOneEmaBelowInPreviousTendency:
					return "BUY"
			else:
				break

		isAtLeastOneEmaAboveInPreviousTendency = False
		for i, ema in enumerate(movingAverages):
			if lastEma[-2] - ema[-2] < 0:
				isAtLeastOneEmaAboveInPreviousTendency = True
			if lastEma[-1] - ema[-1] > 0:
				if i == len(movingAverages)-1 and isAtLeastOneEmaAboveInPreviousTendency:
					return "SELL"
			else:
				break

		return "HOLD"


class Candle:

	openTime = 0
	close = 0
	closeTime = 0

	def __init__(self, json):
		self.openTime = json[0]
		self.close = float(json[4])
		self.closeTime = json[6]



def makeRequest(url, shouldPrintPayload):

	savPrint("Making Request to URL " + url)
	contents = urllib.request.urlopen(url).read()
	parsed = json.loads(contents)

	if shouldPrintPayload:
		savPrint(json.dumps(parsed, indent=3, sort_keys=True))

	return parsed

def savPrint(string, indent = 1):
	indented = ""
	for i in range(indent):
		indented += ">"
	print(" -" + indented + " " + str(string) + "\n")

def toEpoch(date):
	return (date - datetime(1970,1,1)).total_seconds()

savior = Savior().start()

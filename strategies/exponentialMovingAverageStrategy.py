from datetime import datetime, timedelta
from general import toBinanceDateFormat, makeRequest, savPrint
from resources.resources import KlinesResource
from models.candle import CandleFactory
from models.finalAction import FinalAction

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
		json = makeRequest(KlinesResource(self), self.shouldPrintPayload, self.isTesting)
		candles = CandleFactory.candlesWithJson(json)

		movingAverage = []
		for limit in self.limits:
			movingAverage.append(self.ema(candles, limit))

		return self.evaluateMovingAverage(movingAverage), candles[-1]

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

	    if len(candles) < 2*n-2:
	    	savPrint("inappropriate number of candles for EMA", 6)
	    	exit()

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
					return FinalAction.BUY
			else:
				break

		isAtLeastOneEmaAboveInPreviousTendency = False
		for i, ema in enumerate(movingAverages):
			if lastEma[-2] - ema[-2] < 0:
				isAtLeastOneEmaAboveInPreviousTendency = True
			if lastEma[-1] - ema[-1] > 0:
				if i == len(movingAverages)-2 and isAtLeastOneEmaAboveInPreviousTendency:
					return FinalAction.SELL
			else:
				break

		return FinalAction.HOLD
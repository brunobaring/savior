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

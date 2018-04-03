from tests.payload import allData
from resources.constants import ApiIntervalConstant

class TestableData:

	@staticmethod
	def prices():
		candles = allData()
		prices = []
		for candle in candles:
			prices.append(candle.close)
		return prices

	def jsonData():
		return allData()

	def jsonDataWithParamsInUrl(url):

		urlParams = str(url).split("?")[1].split("&")
		startTime = 0
		endTime = 0
		interval = None
		for params in urlParams:
			if "startTime" in params:
				startTime = int(params.split("=")[1])
				continue
			if "endTime" in params:
				endTime = int(params.split("=")[1])
				continue
			if "interval" in params:
				interval = ApiIntervalConstant.objectFor(params.split("=")[1])
		candles = allData()
		json = []

		for i, candle in enumerate(candles):
			if startTime <= int(candle[0]) and int(candle[0]) < endTime:
				if len(json) == 0 or candle[6] - candles[i-1][6] > ApiIntervalConstant.secondsFor(interval):
					json.append(candle)

		return json

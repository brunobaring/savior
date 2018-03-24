from tests.payload import allData


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

	def jsonDataWithParamsInUrl(url):

		urlParams = str(url).split("?")[1].split("&")
		startTime = 0
		endTime = 0
		for params in urlParams:
			if "startTime" in params:
				startTime = int(params.split("=")[1])
				continue
			if "endTime" in params:
				endTime = int(params.split("=")[1])
		candles = allData()
		json = []
		for candle in candles:
			if startTime <= int(candle[0]) and int(candle[0]) < endTime:
				json.append(candle)

		return json

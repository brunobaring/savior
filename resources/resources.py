class Resources:

	baseApi = "https://api.binance.com/api"
	apiVersion = "/v1"
	endpoint = ""
	params = []

	def getUrl(self):
		return self.baseApi + self.apiVersion + self.endpoint + "?" + "&".join(self.params)

class KlinesResource(Resources):

	endpoint = "/klines"
	data = None

	def __init__(self,data):
		self.data = data

	def url(self):
		self.params = [
			"symbol=" + self.data.symbol,
			"interval=" + self.data.interval.value,
			"startTime=" + self.data.startTime,
			"endTime=" + self.data.endTime,
			"limit=" + str(self.data.dataLimit)
		]
		return self.getUrl()


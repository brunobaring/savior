from general import toBinanceDateFormat, toEpoch, savPrint, makeRequest
from datetime import datetime, timedelta
from resources.resources import KlinesResource
from resources.constants import ApiIntervalConstant
from time import sleep
import json
from random import randint

class ApiCollector:


	def __init__(
			self,
			fromYear = 2017,
			fromMonth = 9,
			fromDay = 10,
			fromHour = 8,
			fromMinute = 7,
			toYear = 2017,
			toMonth = 9,
			toDay = 12,
			toHour = 9,
			toMinute = 47,
			interval = ApiIntervalConstant.m1
		):

		self.fromYear = str(fromYear)
		self.fromMonth = str(fromMonth)
		self.fromDay = str(fromDay)
		self.fromHour = str(fromHour)
		self.fromMinute = str(fromMinute)
		self.toYear = str(toYear)
		self.toMonth = str(toMonth)
		self.toDay = str(toDay)
		self.toHour = str(toHour)
		self.toMinute = str(toMinute)

		self.dataLimit = 1000
		self.symbol = "BTCUSDT"
		self.interval = interval
		self.intervalSeconds = ApiIntervalConstant.secondsFor(interval)
		self.startTimeDate = datetime(fromYear, fromMonth, fromDay, fromHour, fromMinute)
		self.endTimeDate = self.startTimeDate + timedelta(seconds=self.intervalSeconds * self.dataLimit - self.intervalSeconds)
		self.endTimeFull = datetime(toYear, toMonth, toDay, toHour, toMinute)

	def start(self):

		while toEpoch(self.endTimeDate) <= toEpoch(self.endTimeFull):

			self.startTime = toBinanceDateFormat(self.startTimeDate)
			self.endTime = toBinanceDateFormat(self.endTimeDate)

			response = makeRequest(KlinesResource(self), False)
			print("pegou " + str(len(response)) + " candles")
			print("de " + str(self.startTimeDate) + " ate " + str(self.endTimeDate) + " candles")

			self.appendToEndOfPayloadFile(response)

			if toEpoch(self.endTimeDate) == toEpoch(self.endTimeFull):
				print("asds")
				break

			minutes = randint(6, 10)
			sleep(minutes * 60)

			self.startTimeDate += timedelta(seconds=self.intervalSeconds * self.dataLimit)
			self.endTimeDate += timedelta(seconds=self.intervalSeconds * self.dataLimit)

			if toEpoch(self.endTimeDate) > toEpoch(self.endTimeFull):
				print("asd")
				self.endTimeDate = self.endTimeFull


		print("loop ended")

	def appendToEndOfPayloadFile(self, payload):
		startTime = self.fromYear + "-" + self.fromMonth + "-" + self.fromDay + "_" + self.fromHour + ":" + self.fromMinute
		endTime = self.toYear + "-" + self.toMonth + "-" + self.toDay + "_" + self.toHour + "-" + self.toMinute
		
		with open("ApiCollectorPayloads/from_" + startTime + "_to_" + endTime + "_withCandle_" + self.interval.value + "_" + self.symbol + ".txt", "w") as myfile:
			json.dump(payload, myfile)





ApiCollector().start()
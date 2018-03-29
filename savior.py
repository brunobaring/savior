 # -*- coding: utf-8 -*-
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from general import savPrint
from strategies.exponentialMovingAverageStrategy import ExponentialMovingAverageStrategy
from tests.testSavior import TestSavior


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
		whatShouldYouDo, candle = exponentialMovingAverageStrategy.whatShouldYouDo()
		savPrint(whatShouldYouDo.value)

	def activateScheduler(self):
		savPrint("Ctrl + C para matar o Savior.")
		scheduler = BlockingScheduler()
		scheduler.add_job(self.whatShouldYouDo, 'interval', seconds=self.schedulerSeconds)
		scheduler.start()

# Savior().start()

testSavior = TestSavior(
	endYear = 2018,
	endMonth = 3,
	endDay = 25,
	endHour = 1,
	startYear = 2016,
	startMonth = 12,
	startDay = 17,
	startHour = 1,
	limits = [13, 21, 55], #Original = [8, 13, 21, 55]
	stopLoss = 10,
	profitTarget = 35
).start()

import enum


class ApiIntervalConstant(enum.Enum):
	
	m1 = "1m"
	m3 = "3m"
	m5 = "5m"
	m15 = "15m"
	m30 = "30m"
	h1 = "1h"
	h2 = "2h"
	h4 = "4h"
	h6 = "6h"
	h8 = "8h"
	h12 = "12h"
	d1 = "1d"
	d3 = "3d"
	w1 = "1w"
	M1 = "1M"


	def objectFor(value):
		for i in list(ApiIntervalConstant):
			if i.value == value:
				return i


	def secondsFor(apiIntervalConstant):
		if apiIntervalConstant == ApiIntervalConstant.m1:
			return 60
		if apiIntervalConstant == ApiIntervalConstant.m3:
			return 180
		if apiIntervalConstant == ApiIntervalConstant.m5:
			return 300
		if apiIntervalConstant == ApiIntervalConstant.m15:
			return 900
		if apiIntervalConstant == ApiIntervalConstant.m30:
			return 1800
		if apiIntervalConstant == ApiIntervalConstant.h1:
			return 3600
		if apiIntervalConstant == ApiIntervalConstant.h2:
			return 7200
		if apiIntervalConstant == ApiIntervalConstant.h4:
			return 14400
		if apiIntervalConstant == ApiIntervalConstant.h6:
			return 21600
		if apiIntervalConstant == ApiIntervalConstant.h8:
			return 28800
		if apiIntervalConstant == ApiIntervalConstant.h12:
			return 43200
		if apiIntervalConstant == ApiIntervalConstant.d1:
			return 86400
		if apiIntervalConstant == ApiIntervalConstant.d3:
			return 259200
		if apiIntervalConstant == ApiIntervalConstant.w1:
			return 604800
		if apiIntervalConstant == ApiIntervalConstant.M1:
			return 2678400



















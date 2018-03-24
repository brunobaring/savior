import pprint
import requests
from datetime import datetime
from tests.testableData import TestableData


def makeRequest(resource, shouldPrintPayload, isTesting = False):

	url = resource.url()

	if isTesting:
		response = TestableData.jsonDataWithParamsInUrl(url)
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


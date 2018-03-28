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
	
def calculateRentability(initialPrice, finalPrice, fees):
	return (finalPrice / initialPrice - 1) * 100 * (1 - fees) #percent

def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]
	
def roundTo(X, n):
	X = float(X)
	pointPos = str(X).find(".")
	if n < len(str(X)[(pointPos+1):]):
		if float(str(X)[n + pointPos + 1]) >= 5:
			x = float(str(X)[0:(pointPos+n+1)]) + float("0." + repeat_to_length("0",n-1)+"1")
			return float(str(x)[0:(pointPos+n+1)])
		else:
			x = float(str(X)[0:(pointPos+n+1)])
			return float(str(x)[0:(pointPos+n+1)])
	else:
		return X
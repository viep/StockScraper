from urllib2 import Request,urlopen,URLError
import mysql.connector
import time
import datetime
import os
import pickle

 # ticker: {
 # 			timestamp:{
 # 						askprice
 # 						bidprice
 # 			}
 # }
def getPrice(ticker):
	req = 'http://finance.yahoo.com/d/quotes.csv?s='+ticker+'&f=ab'
	request= Request(req)
	try:
		resp = urlopen(request)
		data = resp.read()
	except URLError,e:
		print "oops! cant connect"
	data = data.rstrip()
	data = data.split(',')
	val = (float(data[0]),float(data[1]))
	return val
	
def getCurrentTimestamp():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%M-%d %H:%M:%S')
	return st


	###############################
	#### WRITE TO PICKLE ##########
	###############################

def writeToPickle(ticker,timestamp,price):
	try:
			data = pickle.load(open("cisco.p","rb"))
	except (OSError,IOError) as E:
			print "no such file; creating new"
			data = {}

	#read the ticker
	try:
		tickerData = data[ticker]
	except Exception as E:
		print " new ticker "
		data[ticker] = {}
		tickerData = data[ticker]

	tickerData[timestamp] = price
	pickle.dump(data,open("cisco.p","wb"))



def getTickerData(ticker):
	data = {}
	try:
		data = pickle.load(open("cisco.p","rb"))
	except (OSError,IOError) as E:
		print " no file to read from "
		return None

	#read the ticker
	try:
		tickerData = data[ticker]
	except Exception as E:
		print " no such ticker "
		return None
	return tickerData

def getTimestampData(timestamp):
	try:
		data = pickle.load(open("cisco.p","rb"))
	except (OSError,IOError) as E:
		print " no file to read from "
		return None
	timestampData = {}
	for tick,values in data.iteritems():
		for timestamps,prices in values.iteritems():
			 if(timestamps == timestamp):
			 	timestampData[tick] = prices

	return timestampData

def readWholePickle():
	try:
		data = pickle.load(open("cisco.p","rb"))
	except (OSError,IOError) as E:
		print " no such file "
		return None
	return data

#read ticker names from a file and display the data
def getDataForTickers(filename):
	#read each line 
	with open(filename) as tickerNames:
		tickerList = tickerNames.readlines()
	if not tickerList:
		print "empty file "
		return None
	#remove \n and write to pickle
	for eachTicker in tickerList:
		eachTicker = eachTicker.rstrip()
		print "ticker name | "+eachTicker
		## current time stamp to write to pickle 
		st = getCurrentTimestamp()
		##current ask,bid price
		price = getPrice(eachTicker)
		print price
		#write the data to pickle
		writeToPickle(eachTicker,st,price)
		#write the data to database
		writeToDB(eachTicker,st,price)

def writeToDB(ticker,timestamp,price):
	cnx = mysql.connector.connect(user='honeybee', password='honeybee',host = '127.0.0.1',database = 'stocksdb')
	cursor = cnx.cursor()
	valueString = ' VALUES ('+"'"+ticker+"'"+','+"'"+timestamp+"'"+','+str(price[0])+','+str(price[1])+')'
	query = "insert into stocksdb.financialTable (TickerName,Timestamp,AskPrice,BidPrice)"+valueString
	cursor.execute(query)
	cnx.commit()
	cnx.close()


def main():
	#read file with list of tickers and store in pickle prices
	filename = "tickernames.txt"
	getDataForTickers(filename)

	
	## uncomment to get ticker specific data 
	# ## ticker name 
	# ticker = 'YHOO'
	# tickerData = getTickerData(ticker)
	# print tickerData

	#read the whole pickle
	data = readWholePickle()
	print data

	#uncomment to get timestamp specific data
	timestampData = getTimestampData('2016-04-08 01:04:09')
	print timestampData

if __name__ == "__main__": main()



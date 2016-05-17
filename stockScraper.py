
from urllib2 import Request,urlopen,URLError
import mysql.connector
import time
import datetime
import os
import pickle
import pandas as pd
import threading
from pandas.io import sql
from sqlalchemy import create_engine
def getPrice(tickers):
	link = 'http://download.finance.yahoo.com/d/quotes.csv?'
	arguments = 'f=aa2bb2b3b4cc1c3c4c6c8dd1d2ee1e7e8e9ghjkg1g3g4g5g6ii5j1j3j4j5j6k1k2k4k5ll1l2l3mm2m3m4m5m6m7m8nn4opp1p2p5p6qrr1r2r5r6r7ss1s7t1t7t8vv1v7ww1w4xy&amp;'
	req = link+arguments+tickers
	request= Request(req)
	columns = ['a','a2','b','b2','b3','b4','c','c1','c3','c4','c6','c8','d','d1','d2','e','e1','e7','e8','e9','g','h','j','k','g1','g3','g4','g5','g6','i','i5','j1','j3','j4','j5','j6','k1','k2','k4','k5','l','l1','l2','l3','m','m2','m3','m4','m5','m6','m7','m8','n','n4','o','p','p1','p2','p5','p6','q','r','r1','r2','r5','r6','r7','s','s1','s7','t1','t7','t8','v','v1','v7','w','w1','w4','x','y']

	try:
		frameEach = pd.DataFrame(index = None)
		resp = urlopen(request)
		data = resp.read()
		frameEach = pd.read_csv(urlopen(request),header = None)
		
	except URLError,e:
		print "oops! cant connect"
		return None
		return
	#frameEach = pd.concat([frameEach,tickerFrame],axis = 1)
	frameEach.columns = columns
	global tickerFrame
	frameEach['tickerName']=tickerFrame
	st = getCurrentTimestamp()
	frameEach['timestamp'] = st
	print frameEach
	global frame
	frame = frame.append(frameEach)
	return
def getCurrentTimestamp():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%M-%d %H:%M:%S')
	return st

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
#read tickers from file and creates the argument list for  api call
def concatTickers(filename):
	with open(filename) as tickerNames:
		tickerList = tickerNames.readlines()
	if not tickerList:
		print "empty file"
		return None
	tickers = 's='
	global tickerFrame
	fullList = []
	for eachTicker in tickerList:
		eachTicker = eachTicker.rstrip()
		values = eachTicker.split(' ')
		eachTicker = values[-1]
		fullList.append(eachTicker)
		tickers+=eachTicker
		tickers+=','
	tickers = tickers[:-1]
	tickerFrame = pd.DataFrame()
	#dataframe for tickers
	tickerFrame['TickerName'] = fullList
	return tickers

def writeToDB(frame):
	engine = create_engine('mysql+mysqlconnector://honeybee:honeybee@127.0.0.1/stocksdb', echo=False)
	frame.to_sql(name='financialTable', con=engine, if_exists = 'append', index=False)

def job():
	#threading.Timer(1,job).start()

	#runs twice for 300 companies
	while(True):
		global tickers
		getPrice(tickers)
		if(len(frame)==600):
			print "len=600"
			return
		time.sleep(10)

def main():
	global frame
	frame = pd.DataFrame()
	filename = 'tickers300.txt'
	global tickers
	tickers = concatTickers(filename)
	job()
#	frame.to_csv('out.csv',sep = ',')
	assert frame['s'].all() == frame['tickerName'].all()
	frame = frame.astype(object).where(pd.notnull(frame), None)
	writeToDB(frame)

if __name__ == "__main__": main()


	
from pandas import *
from datetime import *
import pdb as pdb

df = DataFrame.from_csv('aapl_1-2012_5min.csv')
dayCount=0
rangeHigh = -1
rangeLow = 9999
openDayRangeDict = {}
getRange = 1
previousDay = 0

upbreak1 = 0
upbreak2 = 0
downbreak1 = 0
downbreak2 = 0

lastClose = 0
maxClose = -1
minClose = 9999
signalCount=0
entryClose = 0

signalDict = {}

for i in range(2,len(df)):
	if dayCount==6:
		dayCount==0
	row = df[(i-1):i]
	currentDay = row.index[0].day
	print row.index[0]
	curClose = row['close'].values[0]
	curOpen = row['open'].values[0]
	#if today's date is different from the previous date
	if not currentDay == previousDay:
		
		#lastClose was yesterday's final closing price
		#store everything: open day range, max close, min close, final close
		if maxClose>0 and upbreak2==1: #if it actually broke up
			signalDay = {}
			signalDay['rangeHigh'] = rangeHigh
			signalDay['rangeLow'] = rangeLow
			signalDay['signalCount'] = signalCount
			signalDay['maxClose'] = maxClose
			signalDay['minClose'] = minClose
			signalDay['entryClose'] = entryClose
			signalDay['finalClose'] = lastClose
			signalDay['type'] = 1
			signalDict[row.index[0]] = signalDay

		if minClose<9999 and downbreak2==1: #if it actually broke down
			signalDay = {}
			signalDay['rangeHigh'] = rangeHigh
			signalDay['rangeLow'] = rangeLow
			signalDay['signalCount'] = signalCount
			signalDay['maxClose'] = maxClose
			signalDay['minClose'] = minClose
			signalDay['entryClose'] = entryClose
			signalDay['finalClose'] = lastClose
			signalDay['type'] = -1
			signalDict[row.index[0]] = signalDay

		print 'last bar was last bar in that day'
	
		#reset all flags
		rangeHigh = -1
		rangeLow = 9999
		maxClose = -1
		minClose = 9999
		dayCount = 0
		signalCount = 0
		getRange = 1
		upbreak1 = 0
		upbreak2 = 0
		downbreak1 = 0
		downbreak2 = 0
		entryClose = 0

	#while we are still in the open day range
	if dayCount<6 and getRange==1:
		if row['high'].values[0]>rangeHigh:
			rangeHigh = row['high'].values[0]
		if row['low'].values[0]<rangeLow:
			rangeLow = row['low'].values[0]
		if dayCount==5:
			openDayRangeDict['high']=rangeHigh
			openDayRangeDict['low']=rangeLow
			getRange=0
			#set_trace() #diagnostic
			#now we have the open day range
		dayCount+=1
	

	#if we already have an open day range, wait for a trade signal
	if getRange==0:
		

		#if we've already had second up break, keep track of max close, min close after that
		if upbreak2==1 or downbreak2==1:
			if curClose>maxClose:
				maxClose = curClose
			if curClose<minClose:
				minClose = curClose
		else:
			signalCount+=1 #count bars b/w open day range and signal
		
		#UP BREAK
		if curClose>openDayRangeDict['high'] and curClose>curOpen:
			if upbreak1==1 and curClose>openDayRangeDict['high'] and curClose>curOpen and curClose>lastClose and downbreak2 == 0:
				#we've gotten a second up day above the range
				upbreak2 = 1
				entryClose = curClose
				#so start keeping track of highest close, as well as close at EOD
				#pdb.set_trace() #diagnostic

			#we've broken above the open day range
			#wait for one more up day
			upbreak1 = 1
			
		else:
			upbreak1 = 0
		
		#DOWN BREAK
		if curClose<openDayRangeDict['low'] and curClose<curOpen:
			if downbreak1==1 and curClose<openDayRangeDict['low'] and curClose<curOpen and curClose<lastClose and upbreak2 == 0:
				#we've gotten a second up day above the range
				downbreak2 = 1
				entryClose = curClose
				#so start keeping track of highest close, as well as close at EOD
				#pdb.set_trace() #diagnostic
			#we've broken above the open day range
			#wait for one more up day
			downbreak1 = 1
			
		else:
			downbreak1 = 0


	previousDay = currentDay
	lastClose = curClose
	
odrDF = DataFrame.from_dict(signalDict)
odrDF = odrDF.T 
odrDF.to_csv("aapl_odr_1-2012.csv")

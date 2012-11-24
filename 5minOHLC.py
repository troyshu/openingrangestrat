from pandas import *
from datetime import *

df = DataFrame.from_csv('aapl_1-2012.csv')
minutes = 5

aggPrices = {}

cur_open = -1
cur_high = -1
cur_low = 9999
cur_close = -1
last_sec = -1

#loop through trades, getting open, high, low, close for every 5 min interval
for i in range(1,len(df)):

	row = df[(i-1):i]
	symbol = row.index[0]
	time = row['TIME'].values[0]
	date = row['DATE'].values[0]
	datetimestr = str(date)+" "+str(time)
	print str(i)+" "+str(datetimestr)

	to_min = int(time.split(':')[1])
	to_sec = int(time.split(':')[2])
	price = row['PRICE'].values[0]
	
	date_object = datetime.strptime(datetimestr,'%Y%m%d %H:%M:%S')

	#if cur open hasn't been set yet, set it
	if cur_open==-1:
		cur_open = price
	if price>cur_high:
		cur_high = price
	if price<cur_low:
		cur_low = price
	#if current minute interval is up
	if to_min%minutes==0 and to_sec==0 and not last_sec==0: 
		cur_close = price
		#add row to dictionary
		row_dict = {}
		

		row_dict['open'] = cur_open
		row_dict['high'] = cur_high
		row_dict['low'] = cur_low
		row_dict['close'] = cur_close
		aggPrices[date_object] = row_dict
		print "added "+str(row_dict)

		cur_open = -1
		cur_high = -1
		cur_low = 9999
		cur_close = -1

	last_sec = to_sec

aggPricesDf = DataFrame.from_dict(aggPrices)
aggPricesDf = aggPricesDf.T
aggPricesDf.to_csv('aapl_1-2012_5min.csv')
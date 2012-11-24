from pandas import *
from datetime import *
import pdb as pdb
import pylab

df = DataFrame.from_csv('aapl_odr_all.csv', sep=";")
model = ols(y=df['maxProfit'], x=df.ix[:,'rangeWidth':'type2'])

model2= ols(y=df['minProfit'], x=df.ix[:,'rangeWidth':'type2'])

model3 = ols(y=df['safeMinProfit'], x=df.ix[:,'rangeWidth':'type2'])

#df.ix[:,'maxProfit':'minProfit'].plot()

grouped = df.groupby('type2')

#long short max profit
lsMaxProfitDict = [0,0]
for name, group in grouped:

	lsMaxProfitDict[name] = group['maxProfit'].values

pylab.boxplot(lsMaxProfitDict)
pylab.xticks([1, 2], ['short', 'long'])

#long short min profit
lsMaxProfitDict = [0,0]
for name, group in grouped:

	lsMaxProfitDict[name] = group['minProfit'].values

pylab.boxplot(lsMaxProfitDict)
pylab.xticks([1, 2], ['short', 'long'])

#histograms of profit vs. rangeWidth, signalCount
#first group by signalCount (discrete)
signalGrouped = df.groupby('signalCountGroup')
signalCount_meanRets = {}
for name, group in signalGrouped:
	signalCount_meanRets[name] = [group['maxProfit'].mean(),group['minProfit'].mean()]


signalGrouped = df.groupby('rangeWidthGroup')
rangeWidth_meanRets = {}
for name, group in signalGrouped:
	rangeWidth_meanRets[name] = [group['maxProfit'].mean(),group['minProfit'].mean()]


rangeWidthRetsDF = DataFrame.from_dict(rangeWidth_meanRets)
rangeWidthRetsDF = rangeWidthRetsDF.T 
rangeWidthRetsDF.columns = ['max profit', 'min profit']
rangeWidthRetsDF.plot(kind='bar', title="Profit vs. Range Width % Quartile")

signalCountRetsDF = DataFrame.from_dict(signalCount_meanRets)
signalCountRetsDF = signalCountRetsDF.T
signalCountRetsDF.columns = ['max profit', 'min profit']
signalCountRetsDF.plot(kind='bar',title="Profit vs. Signal Delay Quartile")

pylab.show()
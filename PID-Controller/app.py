import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import time as tm

waitTimePerTick = .001
dimensions = 20
maxGenerate = 10
minGenerate = -maxGenerate
maxChange = maxGenerate * .3
minChange = -maxChange
currentValue = 0

# Data for plotting
timeInMin = np.arange(0, dimensions + 1, 1.0)
temperture = [20]
for x in range(dimensions):
	randomNumber = rd.uniform(minGenerate,maxGenerate)
	temperture.append(temperture[-1] + randomNumber)

'''
for x in range(dimensions):
	randomNumber = np.sin(2*np.pi*timeInMin) * 20
	temperture.append(int(randomNumber))
'''
#temperture = np.sin(2*np.pi*timeInMin) * 20
#temperture = [20.0, 20.0, 21.0, 21.0, 22.0, 24.0, 24.0, 23.0, 23.0, 25.0, 25.0]

class PIDControl:
	def __init__(self):
		self.oldTime = tm.time()
		self.deltaValue = 0
		self.deltaTime = 1
		self.oldDeltaValue = 0
		tm.sleep(0.001)

	def calculateProportional(self, currentValue, expectedValue, pScale=1):
		return pScale * self.getDeltaValue(currentValue, expectedValue)

	def calculateIntegral(self, currentValue, expectedValue, iScale = 1):
		return iScale * (self.getDeltaValue(currentValue, expectedValue) * self.deltaTime)

	def calculateDerivative(self, currentValue, expectedValue, dScale = 1):
		return dScale * ((self.oldDeltaValue - self.deltaValue) / self.deltaTime)

	def getDeltaValue(self, currentValue, expectedValue):
		self.oldDeltaValue = self.deltaValue
		self.deltaValue = currentValue - expectedValue
		return self.deltaValue

	def getDeltaTime(self):
		self.time = tm.time()
		self.deltaTime = self.time - self.oldTime
		self.oldTime = self.time
		tm.sleep(waitTimePerTick)
		return self.deltaTime

	def getCalculatedPIDValue(self, currentValue, expectedValue):
		self.getDeltaTime()
		self.getDeltaValue(currentValue, expectedValue)
		pidValue = (self.calculateProportional(currentValue, expectedValue) + 
					self.calculateIntegral(currentValue, expectedValue) + 
					self.calculateDerivative(currentValue, expectedValue))
		return pidValue * -1

pid = PIDControl()
pidValues = []

def change(change):
	if change > maxChange:
		change = maxChange
	if change < minChange:
		change = minChange
	return change


sumTime = 0
while True:
	try:
		start = pid.getCalculatedPIDValue(currentValue, temperture[len(pidValues)])
	except:
		break
	start = change(start)
	currentValue += start
	sumTime += pid.deltaTime
	if sumTime > waitTimePerTick:
		print(currentValue)
		sumTime -= waitTimePerTick
		pidValues.append(currentValue)

print(pidValues)

fig, ax = plt.subplots()
ax.set(xlabel='time (male)', ylabel='I am speed (C°)', title='Het is tantoetje koud')
ax.grid()
ax.plot(timeInMin, temperture)
ax.plot(timeInMin, pidValues)

plt.show()
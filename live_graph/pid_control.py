import time as tm
from timer import Sleep as sp
import math as math
from update_file import update_file as uf

#    
#
test = 0
xValue = 0
previousXValue = xValue

def deltaValue(expected_value, current_value):
    deltaValue = expected_value - current_value
    return deltaValue

def calculate_proportional(expected_value, current_value, pScale=1):
    return pScale * deltaValue(expected_value, current_value)

def calculate_integral(expected_value, current_value, iScale = 1):
    deltaIndex = xValue - previousXValue
    return iScale * (deltaValue(expected_value, current_value) * deltaIndex)

def calculate_derivative():
    return 1    

uf().reset()
while True:
    uf().update(xValue,test)

    test = xValue
    test = calculate_proportional(0,test) + calculate_integral(0, test)
    previousXValue = xValue
    xValue = xValue + 1
    sp().sleep(0.1)
import cmath as cm
import math as mt

resistance = float(input("Resistance in Ohm : "))
capacity = float( input("capaity in Farad: "))

frequency = 1
def doeding(resistance,capacity,frequency):
    
    omega = 2*mt.pi*frequency
    zResistor = resistance
    zCapacitor = 1 /(1j *omega*capacity)
    
    amplification = zCapacitor /(zResistor+zCapacitor)
    norm = abs(amplification)
    angle=cm.phase(amplification)
    return (frequency,amplification,norm,angle)

while True:
    frequency *= 1.000000001
    a,b,c,d=doeding(resistance,capacity,frequency)
    print("hier heb je eje rotzooi")
    print (f"freq: {a} ")
    print(f"amp: {b}")
    print(f"norm:{c}")
    print(f"phase:{(180/mt.pi)*d}")
    if c < 0.5:
        
        break




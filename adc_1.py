import machine
import math
from time import sleep
numADCreadings = const(100)
def ADCloopMeanStdDev():
    adc = machine.ADC(0)
    adcread = adc.channel(pin='P18')
    samplesADC = [0.0]*numADCreadings; meanADC = 0.0
    i = 0
    while (i < numADCreadings):
        adcint = adcread()
        samplesADC[i] = adcint
        meanADC += adcint
        i += 1
        time.sleep_ms(1)

    meanADC /= numADCreadings
    varianceADC = 0.0
    for adcint in samplesADC:
        varianceADC += (adcint - meanADC)**2
    varianceADC /= (numADCreadings - 1)
    print("%u ADC readings :\n%s" %(numADCreadings, str(samplesADC)))
    print("Mean of ADC readings (0-1023) = %15.13f" % meanADC)
    print("Mean of ADC readings (0-1000 mV) = %15.13f" % (meanADC*1000/1024))
    print("Variance of ADC readings = %15.13f" % varianceADC)
    print("10**6*Variance/(Mean**2) of ADC readings = %15.13f" % ((varianceADC*10**6)//(meanADC**2)))
    print("Standard deviation of ADC readings = %15.13f" % math.sqrt(varianceADC))

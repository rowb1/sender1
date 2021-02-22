# RP 14FEB2021 - add multiple reads
# BME280_Using I2C at P9, P10, BME280.py mod by RP
#
from network import LoRa
import socket
import time
from machine import I2C, Pin, ADC
from bme280_int import *
# from utime import sleep
import gc


DEVICE_ID=2  #unique ID
NUM_ADC_READS = const(50)

lora = LoRa(mode=LoRa.LORA, region=LoRa.AU915)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)
i = DEVICE_ID
adc=ADC(bits=12)

sw_pin = Pin('P20', Pin.IN)
out_pin = Pin('P21', Pin.OUT)
##adc.init(bits=12)

#batt_pin = adc.channel(pin='P17',attn=ADC.ATTN_0DB)  ##white pin, closest to red pins
#wlvl_pin = adc.channel(pin='P18',attn=ADC.ATTN_0DB)  ##yellow, nearest white pin
#wpress_pin = adc.channel(pin='P16',attn=ADC.ATTN_0DB) ##yellow, at end

i2c=I2C()
bme = BME280(i2c=i2c)
##bme.sealevel=101325

#myPin='P16'

def readADCLoop(myPin):
   adcread = adc.channel(pin=myPin,attn=ADC.ATTN_0DB)
   j = 0
   while (j < NUM_ADC_READS):
       global Av_ADC
       adcint = adcread()
       Av_ADC = Av_ADC + adcint
      # print (adcint,j,Av_ADC,NUM_ADC_READS)
       j += 1
       time.sleep_ms(1)
   Av_ADC /= NUM_ADC_READS
   Av_ADC=int(Av_ADC)
  # print(Av_ADC)

while True:
    i= i+10
    Av_ADC=0
    readADCLoop('P16')
    water_pressure_adc=Av_ADC
    Av_ADC=0
    readADCLoop('P17')
    batt_adc=Av_ADC
    Av_ADC=0
    readADCLoop('P18')
    water_lvl_adc=Av_ADC
    # 25JAN LoRaMessage = String(readingID) + "/" + String(tempC) + "&" + String(humidity) + "#" + String(airPressure)+ "!" + String(wPressure_adc)+ "@" + String(lvl_adc);
    msg=str(i)+"/"+bme.values[0]+"&"+bme.values[2]+"#"+bme.values[1]+"!"+ str(water_pressure_adc) + "@" + str(water_lvl_adc) + "*" + str(batt_adc)
#    pkg = struct.pack(_LORA_PKG_FORMAT % len(msg), DEVICE_ID, len(msg), msg)
    print(msg)
    print('sw_pin.value()=', sw_pin())
    if sw_pin() == 1:
      out_pin.value(1)
      print('out_pin.value()=', out_pin.value())
    else:
      out_pin.value(0)
    #print("analog value=")
    #print(wpress_pin(),wlvl_pin(),batt_pin() )
#    print(pkg)
    lora_sock.send(msg)
    print("msg sent")
    gc.collect()
    #print(bme.values)
    #print(bme.altitude)
    #print(bme.sealevel)
    #print(bme.dew_point)
    #print(bme.values[0])
    #print(bme.humidity)
    #print(bme.pressure)
    time.sleep_ms(5000)

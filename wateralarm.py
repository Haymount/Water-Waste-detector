import RPi.GPIO as GPIO
import datetime
import time
import schedule
from gpiozero import MCP3008
from time import sleep
import math


buzzerpin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerpin, GPIO.OUT, initial=GPIO.LOW)


def checkwatertemp():
    watertemp = 25  
    tmp   = MCP3008(channel=2, device=0)
    while True: 
        adc = (tmp.value *1000)
        adc_1 = (((adc * 3.3 / 1024) -0.5) / 0.01)
  
        ad = (tmp.value)
        print (adc_1)
        sleep(2)

        if watertemp is not None:
            watertemp = adc_1
            print("Current Water temperature is: %d", watertemp)
            if (watertemp > 30):
                GPIO.output(GPIO.HIGH)
            else:
                GPIO.output(GPIO.LOW)
                GPIO.cleanup()
            if (watertemp < 0):
                GPIO.output(GPIO.HIGH)
            else:
                GPIO.output(GPIO.LOW)
                GPIO.cleanup()


#def checkroomtemp():
#roomtemp = 

#while True:
    if roomtemp is not None:
        print("Current Room Temperature is: %d")  

#schedule.every(220).minutes.do(roomtemp)
while True:
    schedule.run_pending()
    time.sleep(220)
    
 
#GPIO.output(buzzerpin, GPIO.HIGH)
#time.sleep(2)
    
#GPIO.output(buzzerpin, GPIO.LOW)

#GPIO.cleanup()






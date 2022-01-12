import RPi.GPIO as GPIO
import datetime
import time
#import schedule
from gpiozero import MCP3008
from time import sleep
import math

GPIO.setmode(GPIO.BCM)
GPIO14 = 14
GPIO.setup(GPIO14, GPIO.OUT, initial=GPIO.LOW)
GPIO.setwarnings(False)
class main:
    def checktemp():
        watertemp = 25

        tmp = MCP3008(channel=2, device=0)

        adc = tmp.value * 1000

        adc_1 = ((adc * 3.3 / 1024) - 0.5) / 0.01

        while True:
            sleep(2)
            if watertemp is not None:
                watertemp = adc_1
                print("Current Water temperature is: ", watertemp)
                if watertemp > 28:
                    GPIO.output(GPIO14, True)
                elif watertemp < 20:
                    GPIO.output(GPIO14, True)
                else:
                    GPIO.output(GPIO14, False)
            else:
                print("No temp")
                GPIO.cleanup()
                break
while True:
    main.checktemp()
#def checkroomtemp():
#roomtemp = 

#while True:
   # if roomtemp is not None:
   #     print("Current Room Temperature is: %d")  

#schedule.every(220).minutes.do(roomtemp)
#while True:
    #schedule.run_pending()
    #time.sleep(220)
    
 
#GPIO.output(buzzerpin, GPIO.HIGH)
#time.sleep(2)
    
#GPIO.output(buzzerpin, GPIO.LOW)

#GPIO.cleanup()






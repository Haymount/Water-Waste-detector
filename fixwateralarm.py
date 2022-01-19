import RPi.GPIO as GPIO
import datetime
import time
import schedule
from gpiozero import MCP3008
from time import sleep

GPIO.setmode(GPIO.BCM)  # Opsætning af RPi.GPIO
GPIO14 = 13  # Pin nummer buzzer
GPIO26 = 26  # Pin nummer rød-led
GPIO19 = 19  # Pin nummer grøn-led
# Sætter pin som output, og starter alarmerne slukket
GPIO.setup([GPIO26, GPIO14, GPIO19], GPIO.OUT, initial=GPIO.LOW)
GPIO.setwarnings(False)
tmp_1 = MCP3008(channel=1, device=0)                  # ADC output
tmp_2 = MCP3008(channel=2, device=0)                  # ADC output

start = datetime.datetime.now()



class var:
    prevtime = 0
    temparr1average = 0
    temparr2average = 0



def tempmaaling():
    
    current_time = time.time()

    timediff = current_time - var.prevtime
    if timediff >= 300:
        # Ganger adc værdi med 1000
        adc_1v = (tmp_1.value * 1000)
        adc_1r = (((adc_1v * 3.3 / 1024) - 0.5) / 0.01)  # Ud regner vandtemp
        # Laver så vi kun får 2 decimaler
        num_1 = round(adc_1r, 2)
        num_1 = int(num_1)

        adc_2v = (tmp_2.value * 1000)                   # Temp på rummet
        # Ganger adc værdi med 1000
        adc_2r = (((adc_2v * 3.3 / 1024) - 0.5) / 0.01)
        num_2 = round(adc_2r, 2)
        num_2 = int(num_2)
       
        return num_1, num_2

    var.prevtime = current_time

    


def tempaverage():
    tempmaaling1, tempmaaling2 = tempmaaling()
   
    temparr1 = []
    temparr2 = []
    
    temparr1.append(tempmaaling1)
    temparr2.append(tempmaaling2)
    
    
    if len(temparr1) >= 12:
        var.temparr1average = sum(temparr1) / len(temparr1)
        return var.temparr1average
        
        
    
    if len(temparr2) >= 12:
        var.temparr2average = sum(temparr2) / len(temparr2)
        return var.temparr2average
    
    

def checkroomtemp():
    roomtemp = 0

    now = datetime.datetime.now()

    if roomtemp is not None:
        roomtemp = tempmaaling[1]
        print(("Room Temp: ", roomtemp), (now.strftime("%d-%m-%Y %H:%M:%S")))


def checkwatertemp(a):  # Funktionen med alt indmaden
    watertempaverage, roomtempaverage = tempaverage()

    now = datetime.datetime.now()

    GPIO.output(GPIO19, True)

    if watertempaverage is not None:
   

        print(("Water Temp: ", watertempaverage), (now.strftime("%d-%m-%Y %H:%M:%S")))
        if abs(watertempaverage - roomtempaverage) <= 0.5:
            GPIO.output(GPIO14, False)
            GPIO.output(GPIO26, False)
        elif watertempaverage < roomtempaverage:  # Hvis temperaturen er UNDER angivet værdi, så går alarmen af
            GPIO.output(GPIO14, True)
            GPIO.output(GPIO26, True)
        elif watertempaverage > roomtempaverage:  # Hvis temperaturen er OVER angivet værdi, så går alarmen af
            GPIO.output(GPIO14, True)
            GPIO.output(GPIO26, True)
        else:  # Hvis temperaturen er i sikker range, er alarmerne slukket
            GPIO.output(GPIO14, False)
            GPIO.output(GPIO26, False)
    else:
        print("No temp")
        GPIO.cleanup()



while True:  # While loop, for at class'en bliver kaldt igen og igen, så længe programmet kører
    tempmaaling()
    checkwatertemp(tempaverage())
    checkroomtemp()

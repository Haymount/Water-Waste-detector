from ast import Or
from typing import Type
import RPi.GPIO as GPIO
import datetime
import time
import schedule
from gpiozero import MCP3008
from time import sleep

GPIO.setmode(GPIO.BCM)  # Opsætning af RPi.GPIO
GPIO13 = 13  # Pin nummer buzzer
GPIO26 = 26  # Pin nummer rød-led
GPIO19 = 19  # Pin nummer grøn-led
GPIO.setup([GPIO26, GPIO13, GPIO19], GPIO.OUT, initial=GPIO.LOW) # Sætter pin som output, og starter alarmerne slukket
GPIO.setwarnings(False)
tmp_1 = MCP3008(channel=1, device=0)                  # ADC output
tmp_2 = MCP3008(channel=2, device=0)                  # ADC output

start = datetime.datetime.now()


class var:
    prevtime = 0.0
    prevtime1 = 0.0
    prevtime2 = 0.0
    prevtime3 = 0.0
    prevtime4 = 0.0
    temparr1average = 0
    temparr2average = 0
    temp1 = 0
    temp2 = 0
    temparr1 = []
    temparr2 = []


def tempaverage():
    current_time = time.time()
    
    if var.prevtime1 == 0.0:
        var.prevtime1 = current_time
        #print("prevtime1" + str(var.prevtime1))

    
    if (current_time - var.prevtime1) >= 2:
        now = datetime.datetime.now()
        #print("tempmaaling")
        adc_1v = (tmp_1.value * 1000)   # Ganger adc værdi med 1000
        adc_1r = (((adc_1v * 3.3 / 1024) - 0.5) / 0.01)  # Ud regner vandtemp
        var.temp1 = round(adc_1r, 2)   # Laver så vi kun får 2 decimaler
        var.temp1 = int(var.temp1)
        #print("temp1 " + str(var.temp1))

        adc_2v = (tmp_2.value * 1000)           # Temp på rummet
        adc_2r = (((adc_2v * 3.3 / 1024) - 0.5) / 0.01)    # Ganger adc værdi med 1000
        var.temp2 = round(adc_2r, 2)
        var.temp2 = int(var.temp2)
        #print("temp2 " + str(var.temp2))

        var.prevtime1 = current_time
    

    var.temparr1.append(var.temp1)
    var.temparr2.append(var.temp2)


    if len(var.temparr1) >= 12:
        var.temparr1average = sum(var.temparr1) / len(var.temparr1)
        # return var.temparr1average
        #print("temparr1" + str(var.temparr1))
        var.temparr1 = []

    if len(var.temparr2) >= 12:
        var.temparr2average = sum(var.temparr2) / len(var.temparr2)
        # return var.temparr2average
        var.temparr2 = []
        #print("temparr2" + str(var.temparr2))
    

    
    watertemp =  "Rørtemp " + str(var.temparr1average),(now.strftime("%d-%m-%Y %H:%M:%S"))
    roomtemp = "Rumtemp " + str(var.temparr2average),(now.strftime("%d-%m-%Y %H:%M:%S"))
  
    
    outfile = open('data.txt', 'a')

        # save the names into the file
    outfile.write(str(watertemp) + '\n')
    outfile.write(str(roomtemp) + '\n')
    
        # close the file
    outfile.close()
    
    return var.temparr1average, var.temparr2average, var.temp1


def checkroomtemp():
    roomtemp = 0

    current_time = time.time()

    if var.prevtime2 == 0.0:
        var.prevtime2 = current_time
   

    if (current_time - var.prevtime2) >= 2:
        if roomtemp is not None:
           a, b, roomtemp = tempaverage()

        var.prevtime2 = current_time


def checkwatertemp():  # Funktionen med alt indmaden
    print("checkwatertemp")
    watertempaverage, roomtempaverage, a = tempaverage()
    
    print("watertempavr" + str(watertempaverage))
    print("roomtempavr" + str(roomtempaverage)) 

    GPIO.output(GPIO19, True)
    current_time = time.time()

    if var.prevtime3 == 0.0:
        var.prevtime3 = current_time

    if (current_time - var.prevtime3) >= 2:
        if watertempaverage is not None:

            
            if abs(watertempaverage - roomtempaverage) <= 5:
                GPIO.output(GPIO26, False)
            elif watertempaverage < roomtempaverage:  # Hvis temperaturen er UNDER angivet værdi, så går alarmen af
                GPIO.output(GPIO26, True)
                buzzerfunc()
            elif watertempaverage > roomtempaverage:  # Hvis temperaturen er OVER angivet værdi, så går alarmen af
                GPIO.output(GPIO26, True)
                buzzerfunc()
            else:  # Hvis temperaturen er i sikker range, er alarmerne slukket
                GPIO.output(GPIO26, False)
        else:
            print("No temp")
            GPIO.cleanup()
        
        var.prevtime3 = current_time
        
def buzzerfunc():
    p = GPIO.PWM(13, 1000)
    p.start(1)
    input('Press return to stop:')   # use raw_input for Python 2
    p.stop()
    GPIO.cleanup()

def debug():
    watertempaverage, roomtempaverage, a = tempaverage()
    now = datetime.datetime.now()
    current_time = time.time()

    if var.prevtime4 == 0.0:
        var.prevtime4 = current_time
    
    if (current_time - var.prevtime4) >=2:
        print(("Water Temp: ", watertempaverage), (now.strftime("%d-%m-%Y %H:%M:%S")))
        print(("Room Temp: ", roomtempaverage), (now.strftime("%d-%m-%Y %H:%M:%S")))
        
        var.prevtime4 = current_time

print("start")
while True:  # While loop, for at class'en bliver kaldt igen og igen, så længe programmet kører
    tempaverage()
    try:
        checkwatertemp()
        checkwatertemp()
        debug()
    except TypeError:
        pass
import RPi.GPIO as GPIO
import datetime
import time
from gpiozero import MCP3008
GPIO.setmode(GPIO.BCM)
GPIO26 = 26
GPIO19 = 19
GPIO13 = 13
GPIO.setup([GPIO26, GPIO19, GPIO13], GPIO.OUT, initial=GPIO.LOW) # Sætter pin som output, og starter alarmerne slukket
GPIO.output(GPIO19, True)
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
    prevtime5 = 0.0
    prevtime6 = 0.0
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
    
    if (current_time - var.prevtime1) >= 300:
        adc_1v = (tmp_1.value * 1000)   # Ganger adc værdi med 1000
        adc_1r = (((adc_1v * 3.3 / 1024) - 0.5) / 0.01)  # Udregner vandtemp
        var.temp1 = round(adc_1r, 2)   # Gør at vi kun får 2 decimaler
        var.temp1 = int(var.temp1)

        adc_2v = (tmp_2.value * 1000)      # Temp på rummet
        adc_2r = (((adc_2v * 3.3 / 1024) - 0.5) / 0.01)    # Ganger adc værdi med 1000
        var.temp2 = round(adc_2r, 2)
        var.temp2 = int(var.temp2)

        var.prevtime1 = current_time
    
    var.temparr1.append(var.temp1)
    var.temparr2.append(var.temp2)

    if len(var.temparr1) >= 12:
        var.temparr1average = sum(var.temparr1) / len(var.temparr1)
        var.temparr1 = []
       
    if len(var.temparr2) >= 12:
        var.temparr2average = sum(var.temparr2) / len(var.temparr2)
        var.temparr2 = []
    
    return var.temparr1average, var.temparr2average, var.temp1

def checkwatertemp():  # Funktionen med alt indmaden
    watertempaverage, roomtempaverage, a = tempaverage()
    
    current_time = time.time()

    if var.prevtime3 == 0.0:
        var.prevtime3 = current_time

    if (current_time - var.prevtime3) >= 3600:
        if watertempaverage is not None:

            
            if abs(watertempaverage - roomtempaverage) <= 2:
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
        
        var.prevtime3 = current_time
        
def buzzerfunc():
    GPIO.setup(GPIO13, GPIO.OUT)
    pwm = GPIO.PWM(13, 1000)
    pwm.start(0.1)
    time.sleep(0.2)
    pwm.ChangeDutyCycle(50)

def debug():
    watertempaverage, roomtempaverage, a = tempaverage()
    now = datetime.datetime.now()
    current_time = time.time()

    if var.prevtime4 == 0.0:
        var.prevtime4 = current_time
    
    if (current_time - var.prevtime4) >= 300:
        print(("Water Temp: ", watertempaverage), (now.strftime("%d-%m-%Y %H:%M:%S")))
        print(("Room Temp: ", roomtempaverage), (now.strftime("%d-%m-%Y %H:%M:%S")))
        
        var.prevtime4 = current_time

def datalog():
    current_time = time.time()

    now = datetime.datetime.now()
    if var.prevtime5 == 0.0:
        var.prevtime5 = current_time

    if (current_time - var.prevtime5) >= 300:
        watertemp =  "Watertemp: " + str(var.temparr1average),(now.strftime("%d-%m-%Y %H:%M:%S"))
        roomtemp = "Roomtemp: " + str(var.temparr2average),(now.strftime("%d-%m-%Y %H:%M:%S"))
        
        outfile = open('data.txt', 'a')
        outfile.write(str(watertemp) + '\n')
        outfile.write(str(roomtemp) + '\n')
        outfile.close()
        var.prevtime5 = current_time

while True:  # While loop, for at class'en bliver kaldt igen og igen, så længe programmet kører
    tempaverage()
    datalog()
    try:
        checkwatertemp()
        debug()
    except TypeError:
        pass
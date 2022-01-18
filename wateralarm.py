import RPi.GPIO as GPIO
import datetime
import time
import schedule
from gpiozero import MCP3008
import threading

GPIO.setmode(GPIO.BCM)                                #Opsætning af RPi.GPIO
GPIO14 = 13                                           #Pin nummer buzzer
GPIO26 = 26                                           #Pin nummer rød-led
GPIO19 = 19                                           #Pin nummer grøn-led
GPIO.setup([GPIO26, GPIO14, GPIO19], GPIO.OUT, initial=GPIO.LOW)        #Sætter pin som output, og starter alarmerne slukket
GPIO.setwarnings(False)
tmp_1 = MCP3008(channel=1, device=0)                  # ADC output
tmp_2 = MCP3008(channel=2, device=0)                  # ADC output


def run_continously(interval=1):
    cease_continous_run = threading.Event()
        
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)
    
    continous_thread = ScheduleThread()
    continous_thread.start()
    return cease_continous_run


class main:                                           #Class for at bruge flere variabler i én funktion

    def checkroomtemp():
        roomtemp = 0

        now = datetime.datetime.now()

        adc_2v = (tmp_2.value *1000)                   # Temp på rummet
        adc_2r = (((adc_2v * 3.3 / 1024) -0.5) / 0.01) # Ganger adc værdi med 1000
        num_2 = round(adc_2r, 2)  
        num_2 = int(num_2)

        if roomtemp is not None:
            roomtemp = num_2
            print(("Room Temp: ", roomtemp), (now.strftime("%d-%m-%Y %H:%M:%S")))
            return num_2
    #schedule.every().hour.do(checkroomtemp)
    schedule.every(10).seconds.do(checkroomtemp())

          
       
    def checktemp(a):                                  #Funktionen med alt indmaden
            watertemp = 0                              #Giver watertemp en start værdi
            roomtemp = a
            
                                                             # temp på rør 
            adc_1v = (tmp_1.value *1000)                   # Ganger adc værdi med 1000
            adc_1r = (((adc_1v * 3.3 / 1024) -0.5) / 0.01) # Ud regner vandtemp
            num_1 = round(adc_1r, 2)                      # Laver så vi kun får 2 decimaler
            num_1 = int(num_1)
            now = datetime.datetime.now()
            
            GPIO.output(GPIO19, True)
            schedule.every(2).seconds.do(adc_1v)

            if watertemp is not None:
                watertemp = num_1                            #watertemp værdien bliver erstattet af temperaturmålerens aflæsnings-værdi
                
                print(("Water Temp: ", watertemp), (now.strftime("%d-%m-%Y %H:%M:%S")))
                if watertemp > 30:                           #Hvis temperaturen er OVER angivet værdi, så går alarmen af
                    GPIO.output(GPIO14, True)
                    GPIO.output(GPIO26, True)
                elif watertemp < 22:                         #Hvis temperaturen er UNDER angivet værdi, så går alarmen af
                    GPIO.output(GPIO14, True)
                    GPIO.output(GPIO26, True)
                elif abs(watertemp - roomtemp) <= 3:
                    GPIO.output(GPIO14, False)
                    GPIO.output(GPIO26, False)
                elif watertemp > roomtemp:
                    GPIO.output(GPIO14, True)
                    GPIO.output(GPIO26, True)
                elif watertemp < roomtemp: 
                    GPIO.output(GPIO14, True)
                    GPIO.output(GPIO26, True)
                else:                                        #Hvis temperaturen er i sikker range, er alarmerne slukket
                    GPIO.output(GPIO14, False)
                    GPIO.output(GPIO26, False)      
            else:
                print("No temp")
                GPIO.cleanup()
    with open("test.txt", "w") as file: # xyz.txt is filename, w means write format
        file.write("test") 
  
        f= open("test.txt", "w")
        f.write(num_1, num_2)
        f.close()# write text xyz in the file


while True:                                                  #While loop, for at class'en bliver kaldt igen og igen, så længe programmet kører
  main.checkroomtemp()
  main.checktemp(main.checkroomtemp())
  schedule.run_pending()
  time.sleep(1)
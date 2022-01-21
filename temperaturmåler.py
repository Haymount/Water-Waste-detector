from gpiozero import MCP3008
from time import sleep
import math 
import datetime 
def temp():
  tmp_1      = MCP3008(channel=1, device=0)             # ADC output
  tmp_2      = MCP3008(channel=2, device=0)             # ADC output

  while True:                                        # Temp som er på rør
    adc_1v   = (tmp_1.value *1000)                   # Ganger adc værdi med 1000
    adc_1r   = (((adc_1v * 3.3 / 1024) -0.5) / 0.01) # Ud regner temp
    num_1    = round(adc_1r, 2)                      # Laver så vi kun får 2 decimaler
  
    now = datetime.datetime.now()
  
  
    adc_2v   = (tmp_2.value *1000)                   # Temp på rumet
    adc_2r   = (((adc_2v * 3.3 / 1024) -0.5) / 0.01) # Ganger adc værdi med 1000
    num_2    = round(adc_2r, 2)                      # Ud regner temp
    print ( num_2, (now.strftime("%d-%m-%Y %H:%M:%S")))   # Laver så vi kun får 2 decimaler  
    print ( num_1, (now.strftime("%d-%m-%Y %H:%M:%S")))
    sleep(2)  
   
temp()
  
  rortemp =  "Rørtemp " + str(num_1),(now.strftime("%d-%m-%Y %H:%M:%S"))
  rumtemp = "Rumtemp " + str(num_1),(now.strftime("%d-%m-%Y %H:%M:%S"))
  
    
  outfile = open('data.txt', 'a')

  # save the names into the file
  outfile.write(str(rortemp) + '\n')
  outfile.write(str(rumtemp) + '\n')
    
  # close the file
  outfile.close()
  
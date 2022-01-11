from gpiozero import MCP3008
from time import sleep
import math



tmp   = MCP3008(channel=2, device=0)
while True: 
  adc   = (tmp.value *1000)
  adc_1 = (((adc * 5.0 / 1024) -0.5) / 0.01)
  
  ad    = (tmp.value)
  print (adc_1)
  sleep(2)
  
 
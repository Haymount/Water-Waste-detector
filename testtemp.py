from gpiozero import MCP3008
from time import sleep
import math

tmp   = MCP3008(channel=2, device=0)

while True: 
  adc   = (tmp.value *1000)
  adc_1   = (((adc * 3.3 / 1024) -0.5) / 0.01)
  num = round(adc_1, 2)
  print ( num)
  
  sleep(2)
  
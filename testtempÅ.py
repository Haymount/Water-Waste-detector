from gpiozero import MCP3008
from time import sleep
import math

tmp_1      = MCP3008(channel=1, device=0)             # ADC output
tmp_2      = MCP3008(channel=2, device=0)             # ADC output

while True:                                        # Temp som er på rør
  adc_1v   = (tmp_1.value *1000)                   # Ganger adc værdi med 1000
  adc_1r   = (((adc_1v * 3.3 / 1024) -0.5) / 0.01) # Ud regner temp
  num_1    = round(adc_1r, 2)                      # Laver så vi kun får 2 decimaler
  print ( num_1)
  
  adc_2v   = (tmp_2.value *1000)                   # Temp på rumet
  adc_2r   = (((adc_2v * 3.3 / 1024) -0.5) / 0.01) # Ganger adc værdi med 1000
  num_2    = round(adc_2r, 2)                      # Ud regner temp
  print ( num_2)                                   # Laver så vi kun får 2 decimaler  
  
  sleep(2)
  
  
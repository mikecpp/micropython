import pyb
from oled1602 import OLED1602

lcd = OLED1602()
lcd.init()

lcd.cursor(0, 0)
lcd.puts("Hello Mike")

count = 0
while(True):
    lcd.cursor(0, 1)
    msg = 'Count = ' + str(count)
    lcd.puts(msg)
    count += 1
    pyb.delay(1000)

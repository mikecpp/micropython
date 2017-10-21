from max7219 import Matrix8x8
from machine import Pin, SPI
from pyb import delay

spi     = SPI(1)
display = Matrix8x8(spi, Pin('A4'), 10)
display.brightness(1)
display.text('0123456789', 0, 0)

while(True):
    display.scroll(1, 0)
    display.show()
    delay(100)
    
from max7219 import Matrix8x8
from machine import Pin, SPI
from pyb import delay

spi     = SPI(1)
display = Matrix8x8(spi, Pin('A4'), 1)

display.brightness(1)

display.fill(1)
display.show()
delay(2000)

display.pixel(0,0,1)
display.pixel(1,1,1)
display.hline(0,4,8,1)
display.vline(4,0,8,1)
display.line(8, 0, 16, 8, 1)
display.rect(17,1,6,6,1)
display.fill_rect(25,1,6,6,1)
display.show()
delay(2000)

display.fill(0)
display.text('dead',0,0,1)
display.text('beef',32,0,1)
display.show()
delay(2000)

display.fill(0)
display.text('12345678',0,0,1)
display.show()
display.scroll(-8,0) # 23456788
display.scroll(-8,0) # 34567888
display.show()
delay(2000)

import pyb
from ssd1306 import SSD1306

display = SSD1306()
display.poweron()
display.init_display()

display.draw_text(10, 10, "Hello Mike")
display.display()
pyb.delay(2000)

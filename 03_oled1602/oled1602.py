import pyb

LCD_DISPLAYON           = 0x04
LCD_CURSOROFF           = 0x00
LCD_BLINKOFF            = 0x00
LCD_2OR4LINE            = 0x08
LCD_DOUBLEHEIGHTOFF     = 0x00
LCD_EXTENSIONREGISTERON = 0x02
LCD_FUNCTIONSET         = 0x20 
LCD_RETURNHOME          = 0x02
LCD_CLEARDISPLAY        = 0x01

ADDR = 0x3C

class OLED1602:
    def __init__(self):
        self.i2c     = pyb.I2C(1)
        self.i2c.init(pyb.I2C.MASTER)
        self.addr    = ADDR
        self.buffer  = bytearray(2)
        self.displaycontral  = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.displayfunction = LCD_2OR4LINE  | LCD_DOUBLEHEIGHTOFF
        self.rawoffset = [0x00, 0x40, 0x40, 0x60]

    def command(self, value):
        self.buffer[0] = 0x00
        self.buffer[1] = value
        self.i2c.send(self.buffer, addr = self.addr, timeout = 5000)
    
    def data(self, value):
        self.buffer[0] = 0x40
        self.buffer[1] = value
        self.i2c.send(self.buffer, addr = self.addr, timeout = 5000)
        
    def setRE(self):
        self.displayfunction |= LCD_EXTENSIONREGISTERON
        self.command(LCD_FUNCTIONSET | self.displayfunction)
    
    def clearRE(self):
        self.displayfunction &= ~LCD_EXTENSIONREGISTERON
        self.command(LCD_FUNCTIONSET | self.displayfunction)
        
    def set_contrast(self, value):
        self.setRE();
        self.command(0x79)
        self.command(0x81)
        self.command(value)
        self.command(0x78)
        self.clearRE();

    def init(self):
        # Enable internal regulator
        self.command(0x2A)
        self.command(0x71)
        self.data(0x5C)
        self.command(0x28)
        
        # Set display off
        self.command(0x08)
        
        # Set display clock divide rate
        self.command(0x2A)
        self.command(0x79)
        self.command(0xD5)
        self.command(0x70)
        self.command(0x78)
        
        # Set 1~2 lines
        self.command(0x08)
        
        # Set Re-MAP mode
        self.command(0x06)
        
        # CGRAM
        self.command(0x72)
        self.data(0x05)
        
        # Set OLED characterization
        self.command(0x79)
        
        # set SEG pins
        self.command(0xDA)
        self.command(0x10)
        self.command(0xDC)
        self.command(0x03)
        
        # Contrast
        self.command(0x81)
        self.command(0xFF)
        
        # Set Pre-Charge period
        self.command(0xD9)
        self.command(0xF1)
        
        # Set VCOMH dis-select level
        self.command(0xDB)
        self.command(0x40)
        
        # Exit OLED characterization
        self.command(0x78)
        self.command(0x28)
        
        # Set display off
        self.command(0x08)
        
        # Clear display
        self.command(0x01)
        
        # Set DDRAM address
        self.command(0x80)
        
        # Turn ON display
        self.command(0x0C)
               
        self.set_contrast(0x10)
        self.clear()
        
    def home(self):
        self.command(LCD_RETURNHOME)
    
    def clear(self):
        self.command(LCD_CLEARDISPLAY)
    
    def cursor(self, col, row):
        self.command(0x80 | (col + self.rawoffset[row]))
    
    def puts(self, string):
        for ch in string:
            self.data(ord(ch))
        
    

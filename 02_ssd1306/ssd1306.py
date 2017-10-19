import pyb
import font

# Constants
DISPLAYOFF          = 0xAE
SETCONTRAST         = 0x81
DISPLAYALLON_RESUME = 0xA4
DISPLAYALLON        = 0xA5
NORMALDISPLAY       = 0xA6
INVERTDISPLAY       = 0xA7
DISPLAYON           = 0xAF
SETDISPLAYOFFSET    = 0xD3
SETCOMPINS          = 0xDA
SETVCOMDETECT       = 0xDB
SETDISPLAYCLOCKDIV  = 0xD5
SETPRECHARGE        = 0xD9
SETMULTIPLEX        = 0xA8
SETLOWCOLUMN        = 0x00
SETHIGHCOLUMN       = 0x10
SETSTARTLINE        = 0x40
MEMORYMODE          = 0x20
COLUMNADDR          = 0x21
PAGEADDR            = 0x22
COMSCANINC          = 0xC0
COMSCANDEC          = 0xC8
SEGREMAP            = 0xA0
CHARGEPUMP          = 0x8D
EXTERNALVCC         = 0x10
SWITCHCAPVCC        = 0x20
SETPAGEADDR         = 0xB0
SETCOLADDR_LOW      = 0x00
SETCOLADDR_HIGH     = 0x10
ACTIVATE_SCROLL                      = 0x2F
DEACTIVATE_SCROLL                    = 0x2E
SET_VERTICAL_SCROLL_AREA             = 0xA3
RIGHT_HORIZONTAL_SCROLL              = 0x26
LEFT_HORIZONTAL_SCROLL               = 0x27
VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
VERTICAL_AND_LEFT_HORIZONTAL_SCROLL  = 0x2A

DEVID   = 0x3c
CTL_CMD = 0x80
CTL_DAT = 0x40

class SSD1306():
  def __init__(self):
    self.height       = 64
    self.pages        = int(self.height / 8)
    self.columns      = 128
    self.external_vcc = False

    self.i2c     = pyb.I2C(1)
    self.i2c.init(pyb.I2C.MASTER, baudrate=400000) # 400kHz
    self.devid   = DEVID
    self.offset  = 1
    self.cbuffer = bytearray(2)
    self.cbuffer[0] = CTL_CMD

  def clear(self):
    self.buffer = bytearray(self.offset + self.pages * self.columns)
    if self.offset == 1:
      self.buffer[0] = CTL_DAT

  def write_command(self, command_byte):
    if self.offset == 1:
      self.cbuffer[1] = command_byte
      self.i2c.send(self.cbuffer, addr=self.devid, timeout=5000)
    else:
      self.dc.low()
      self.spi.send(command_byte)

  def invert_display(self, invert):
    self.write_command(INVERTDISPLAY if invert else NORMALDISPLAY)

  def display(self):
    self.write_command(COLUMNADDR)
    self.write_command(0)
    self.write_command(self.columns - 1)
    self.write_command(PAGEADDR)
    self.write_command(0)
    self.write_command(self.pages - 1)
    if self.offset == 1:
      self.i2c.send(self.buffer, addr=self.devid, timeout=5000)
    else:
      self.dc.high()
      self.spi.send(self.buffer)

  def set_pixel(self, x, y, state):
    index = x + (int(y / 8) * self.columns)
    if state:
      self.buffer[self.offset + index] |= (1 << (y & 7))
    else:
      self.buffer[self.offset + index] &= ~(1 << (y & 7))

  def init_display(self):
    chargepump = 0x10 if self.external_vcc else 0x14
    precharge  = 0x22 if self.external_vcc else 0xf1
    multiplex  = 0x1f if self.height == 32 else 0x3f
    compins    = 0x02 if self.height == 32 else 0x12
    contrast   = 0xff # 0x8f if self.height == 32 else (0x9f if self.external_vcc else 0x9f)
    data = [DISPLAYOFF,
            SETDISPLAYCLOCKDIV, 0x80,
            SETMULTIPLEX, multiplex,
            SETDISPLAYOFFSET, 0x00,
            SETSTARTLINE | 0x00,
            CHARGEPUMP, chargepump,
            MEMORYMODE, 0x00,
            SEGREMAP | 0x10,
            COMSCANDEC,
            SETCOMPINS, compins,
            SETCONTRAST, contrast,
            SETPRECHARGE, precharge,
            SETVCOMDETECT, 0x40,
            DISPLAYALLON_RESUME,
            NORMALDISPLAY,
            DISPLAYON]
    for item in data:
      self.write_command(item)
    self.clear()
    self.display()

  def poweron(self):
    if self.offset == 1:
      pyb.delay(10)
    else:
      self.res.high()
      pyb.delay(1)
      self.res.low()
      pyb.delay(10)
      self.res.high()
      pyb.delay(10)

  def poweroff(self):
    self.write_command(DISPLAYOFF)

  def contrast(self, contrast):
    self.write_command(SETCONTRAST)
    self.write_command(contrast)

  def draw_text(self, x, y, string, size=1, space=1):
    def pixel_x(char_number, char_column, point_row):
      char_offset = x + char_number * size * font.cols + space * char_number
      pixel_offset = char_offset + char_column * size + point_row
      return self.columns - pixel_offset

    def pixel_y(char_row, point_column):
      char_offset = y + char_row * size
      return char_offset + point_column

    def pixel_mask(char, char_column, char_row):
      char_index_offset = ord(char) * font.cols
      return font.bytes[char_index_offset + char_column] >> char_row & 0x1

    pixels = (
      (pixel_x(char_number, char_column, point_row),
       pixel_y(char_row, point_column),
       pixel_mask(char, char_column, char_row))
      for char_number, char in enumerate(string)
      for char_column in range(font.cols)
      for char_row in range(font.rows)
      for point_column in range(size)
      for point_row in range(1, size + 1))

    for pixel in pixels:
      self.set_pixel(*pixel)
      
from machine import I2C, Pin
import time
from lcd_i2c_api.lcd_2004a_api import LCDAPI
from lcd_i2c_api.pcf8574t_wrapper import PCF8574I2C

class I2CLCD(PCF8574I2C, LCDAPI):
    
    def __init__(self, scl, sda, i2c_addr, rows, columns):
        self._i2c = I2C(scl=Pin(scl), sda=Pin(sda))
        self._i2c_addr = i2c_addr
        self.rows = rows
        self.cols = columns
        self.curr_column = 0
        self.curr_row = 0
        
        # Calling init function in LCDAPI
        self._init()
        
        # Creating lines addresses objects
        self._display_addresses(rows, columns)

    def Print(self, str):
        for ch in str:
            self._newline_check()
            self._wr_data(ord(ch))
            self.curr_column += 1
    
    def exit_handling(self):
        self.clear()

if __name__ == '__main__':
    lcd = I2CLCD(5, 4, 0x27, 4, 20)
    
    pass
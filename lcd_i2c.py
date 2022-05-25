from machine import I2C, Pin
import time
from lcd_i2c_api.lcd_2004a_api import LCDAPI
from lcd_i2c_api.pcf8574t_wrapper import PCF8574I2C

class I2CLCD(PCF8574I2C, LCDAPI):
    
    def __init__(self, scl, sda, i2c_addr):
        self._i2c = I2C(scl=Pin(scl), sda=Pin(sda))
        self._i2c_addr = i2c_addr
        
        # Initializing whatever in LCDAPI
        self._init()

    # def instr_set(self, instr):
    #     bts = bytearray(1)
    #     bts[0] = instr
    #     return bts
    
    # def _wr_cmd(self, instr):
        
    #     # Preparing data for 4-bit operation
    #     # Sending one byte of information in 2 pieces (nibbles)
    #     # Sending 4 higher bites and then 4 lower bites
        
    #     # Higher nibble (4 bits)
    #     instr_high = instr & 0xF0 | self.D3
    #     self._wr_nibble(instr_high)
        
    #     # Lower nibble (4 bits)
    #     instr_low = (instr & 0x0F) << 4 | self.D3
    #     self._wr_nibble(instr_low)

    # def _shift_cursor(self):
    #     self._wr_cmd(self.D4 | self.D2)

    # def _wr_data(self, instr):
        
    #     # Preparing data for 4-bit operation
    #     # Sending one byte of information in 2 pieces (nibbles)
    #     # Sending 4 higher bites and then 4 lower bites
        
    #     # Higher nibble (4 bits)
    #     instr_high = self.RS | instr & 0xF0 | self.D3 # RS high and R/W to Low
    #     self._wr_nibble(instr_high)
        
    #     # Lower nibble (4 bits)
    #     instr_low = self.RS | self.D3 | (instr & 0x0F) << 4
    #     self._wr_nibble(instr_low)

    # def _init(self):
        
    #     # self._i2c.writeto(self._i2c_addr, bytes(0x00))
        
    #     # Let LCD to power up
    #     time.sleep_ms(20)
        
    #     # Instruction set
    #     for _ in range(3):
    #         self._wr_nibble(self.D5 | self.D4)
    #         time.sleep_ms(5)
        
    #     # 4 bit mode
    #     self._wr_nibble(self.D5)
    #     self._wr_nibble(self.D5)

    #     self._wr_nibble(self.D7 | self.D6)
    #     self._wr_nibble(0x00)
    #     self._wr_nibble(self.D7)
    #     self._wr_nibble(0x00)
    #     self._wr_nibble(self.D4)
    #     self._wr_nibble(0x00)
    #     self._wr_nibble(self.D6 | self.D5)

    #     # Display ON and HOME
    #     self._wr_cmd(self.D3 | self.D2)

    # def clear_display(self):
    #     self._wr_cmd(self.D0)
    #     self._wr_cmd(self.D1)
    #     self._wr_cmd(self.D3)

    def Print(self, str):
        for ch in str:
            self._wr_data(ord(ch))
    
    def exit_handling(self):
        self.clear()
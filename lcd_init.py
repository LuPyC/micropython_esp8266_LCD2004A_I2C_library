import sys
# import time
# from machine import I2C, Pin
from lcd_i2c import I2CLCD


# class I2CLCD:
        
#     # ADDRESSES DEFINITION

#     ENABLE = 0x04
#     RS = 0x01
#     RW = 0x02

#     D0 = 0x01
#     D1 = 0x02
#     D2 = 0x04
#     D3 = 0x08
#     D4 = 0x10
#     D5 = 0x20
#     D6 = 0x40
#     D7 = 0x80
    
#     def __init__(self, scl, sda, i2c_addr):
#         self._i2c = I2C(scl=Pin(5), sda=Pin(4))
#         self._i2c_addr = i2c_addr
#         self._init()
    
#     def _wr_nibble(self, instr):
#         # Writing a nibble (4 bits) of data
#         self._i2c.writeto(self._i2c_addr, self.instr_set(self.ENABLE | instr))
#         # time.sleep_ms(5)
#         self._i2c.writeto(self._i2c_addr, self.instr_set(instr))
#         time.sleep_ms(1)

#     def instr_set(self, instr):
#         bts = bytearray(1)
#         bts[0] = instr
#         return bts
    
#     def _wr_cmd(self, instr):
        
#         # Preparing data for 4-bit operation
#         # Sending one byte of information in 2 pieces (nibbles)
#         # Sending 4 higher bites and then 4 lower bites
        
#         # Higher nibble (4 bits)
#         instr_high = instr & 0xF0 | self.D3
#         self._wr_nibble(instr_high)
        
#         # Lower nibble (4 bits)
#         instr_low = (instr & 0x0F) << 4 | self.D3
#         self._wr_nibble(instr_low)

#     def _shift_cursor(self):
#         self._wr_cmd(self.D4 | self.D2)

#     def _wr_data(self, instr):
        
#         # Preparing data for 4-bit operation
#         # Sending one byte of information in 2 pieces (nibbles)
#         # Sending 4 higher bites and then 4 lower bites
        
#         # Higher nibble (4 bits)
#         instr_high = self.RS | instr & 0xF0 | self.D3 # RS high and R/W to Low
#         # pcf.port = self.ENABLE | instr_high
#         self._wr_nibble(instr_high)
#         # time.sleep_ms(5)
#         # pcf.port = instr_high
#         # time.sleep_ms(1)
        
#         # Lower nibble (4 bits)
#         instr_low = self.RS | self.D3 | (instr & 0x0F) << 4
#         self._wr_nibble(instr_low)
#         # pcf.port = self.ENABLE | instr_low
#         # time.sleep_ms(5)
#         # pcf.port = instr_low
#         # time.sleep_ms(1)

#     def _init(self):
        
#         self._i2c.writeto(self._i2c_addr, bytes(0x00))
        
#         # Let LCD to power up
#         time.sleep_ms(100)
        
#         # Instruction set
#         for _ in range(3):
#             self._wr_nibble(self.D5 | self.D4)
#             time.sleep_ms(5)
        
#         # 4 bit mode
#         self._wr_nibble(self.D5)
#         # time.sleep_ms(1)
        
#         self._wr_nibble(self.D5)
#         self._wr_nibble(self.D7 | self.D6)
#         self._wr_nibble(0x00)
#         self._wr_nibble(self.D7)
#         self._wr_nibble(0x00)
#         self._wr_nibble(self.D4)
#         self._wr_nibble(0x00)
#         # self._wr_nibble(self.D5)
#         # self.clear_display()
#         self._wr_nibble(self.D6 | self.D5)

#         self._wr_cmd(self.D3 | self.D2)
        
#         # self._wr_nibble(0x00)
#         # self._wr_nibble(self.D7 | self.D6)
#         # self._wr_nibble(0x00)
#         # self._wr_cmd(self.D5)
#         # self.clear_display()

#     def clear_display(self):
#         self._wr_cmd(self.D1)
#         self._wr_cmd(self.D2)

#     def Print(self, str):
#         for ch in str:
#             print(ch)
#             self._wr_data(ord(ch))
    
#     def exit_handling(self):
#         self._init()

# I2C INITIALIZATION
lcd = I2CLCD(5, 4, 0x27)

pp = 'abcd'

lcd.Print(pp)

while True:
    try:
        cch = input("Insert data: ")
        lcd.Print(cch)
    except KeyboardInterrupt:
        lcd.exit_handling()
        break
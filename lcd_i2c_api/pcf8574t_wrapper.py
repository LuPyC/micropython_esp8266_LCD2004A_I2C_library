# ADDRESSES DEFINITION

ENABLE = 0x04
RS = 0x01
RW = 0x02

class PCF8574I2C:
    def __init__(self):
        # To be defined in the child class.
        # !!!!!BEWARE OF NAMES!!!!!
        self._i2c = None
        self._i2c_addr = None
    
    def _wr_nibble(self, instr):
        # Writing a nibble (4 bits) of data
        self._i2c.writeto(self._i2c_addr, self._instr_set(ENABLE | instr))
        self._i2c.writeto(self._i2c_addr, self._instr_set(instr))

    def _i2c_read(self):
        # Reading 1 byte from peripheral
        return self._i2c.readfrom(self._i2c_addr, 1)[0]
    
    def _instr_set(self, instr):
        bts = bytearray(1)
        bts[0] = instr
        return bts
    
    def _wr_cmd(self, instr):
        # Preparing data for 4-bit operation
        # Sending one byte of information in 2 pieces (nibbles)
        # Sending 4 higher bites and then 4 lower bites
        
        # Higher nibble (4 bits)
        instr_high = instr & 0xF0 | self.D3
        self._wr_nibble(instr_high)
        
        # Lower nibble (4 bits)
        instr_low = (instr & 0x0F) << 4 | self.D3
        self._wr_nibble(instr_low)

    def _wr_data(self, instr):
        
        # Preparing data for 4-bit operation
        # Sending one byte of information in 2 pieces (nibbles)
        # Sending 4 higher bites and then 4 lower bites
        
        # Higher nibble (4 bits)
        instr_high = RS | instr & 0xF0 | self.D3 # RS high and R/W to Low
        self._wr_nibble(instr_high)
        
        # Lower nibble (4 bits)
        instr_low = RS | self.D3 | (instr & 0x0F) << 4
        self._wr_nibble(instr_low)
    
    def check_busy(self):
        # Checks busy flag (pg. 9)
        # I need to pull RW high to enable read operation
        # Busy Flag will be on D7 (MSB)
        self._wr_nibble(RW)          # CAREFUL ABOUT THIS, causes recursive call
        
        # Converting byte to raw bit format (e.g. 01011010)
        bits = f'{self._i2c_read():0>8b}'
        
        # Checking MSB and returning True if busy, else otherwise
        return True if bool(int(bits[0])) else False
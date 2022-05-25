import time

D0 = 0x01
D1 = 0x02
D2 = 0x04
D3 = 0x08
D4 = 0x10
D5 = 0x20
D6 = 0x40
D7 = 0x80

class LCDAPI:
    
    # Needed by wrapper
    D3 = 0x08
    
    # Basic writing functions.
    def _wr_nibble(self, instr):
        # Writing a nibble (4 bits) of data
        
        # This method should be implemented in child class
        
        raise NotImplementedError("This method must be implemented in child class.")
    
    def _wr_cmd(self):
        # Writing command to i2c slave
        
        raise NotImplementedError("This method must be implemented in child class.")
    
    def _wr_data(self):
        
        # Writing data to i2c slave
        
        raise NotImplementedError("This method must be implemented in child class.")

    def _init(self):
        """ 
        Initialization procedure. 
        As written in datasheet, this is the exact sequence of commands needed to 
        correctly initialize the LCD.
        
        Reference: initializing by instruction, page 48
        """
        
        # Let LCD to power up
        time.sleep_ms(20)
        
        # Instruction set
        for _ in range(3):
            self._wr_nibble(D5 | D4)
            time.sleep_ms(5)
        
        # 4 bit mode
        self._wr_nibble(D5)
        self._wr_nibble(D5)

        self._wr_nibble(D7 | D6)
        self._wr_nibble(0x00)
        self._wr_nibble(D7)
        self._wr_nibble(0x00)
        self._wr_nibble(D4)
        self._wr_nibble(0x00)
        self._wr_nibble(D6 | D5)

        # Initialization ends here
        
        # Display ON and HOME
        self._wr_cmd(D3 | D2)

    # Basic low-level functions 

    def clear(self):
        # Defines Clear Display (pg. 41)
        self._wr_cmd(D0)
    
    def home(self):
        # Defines Return Home (pg. 41)
        self._wr_cmd(D1)
    
    def entry_mode_set(self, shift_direction='R', shift_enable=True):
        # Defines Entry Mode Set (pg. 41)
        if not shift_direction in ['R', 'L']:
            raise ValueError(f"'shift_direction' value {shift_direction} is not supported.\n Accepted values are 'R' (right) or 'L' (left).")
        if not type(shift_enable) is bool:
            raise TypeError(f"'shift_enable' value must be a bool (True, False).")
        
        cmd = D2
        if shift_enable:
            cmd |= D0
            if shift_direction == 'L':
                cmd |= D1
        self._wr_cmd(cmd)
    
    def display_control(self, status:bool, cursor_enable=False, cursor_blink=False):
        # Defines ON/OFF (pg. 42)
        if not type(cursor_enable) is bool:
            raise TypeError(f"'cursor_enable' value must be a bool (True, False).")
        if not type(cursor_blink) is bool:
            raise TypeError(f"'cursor_blink' value must be a bool (True, False).")
        cmd = D3
        if status:
            cmd |= D2
        
        if cursor_enable:
            cmd |= D1
            
        if cursor_blink:
            cmd |= D0
        
        self._wr_cmd(cmd)
    
    def shift_data(self, which='cursor', direction='R'):
        if not direction in ['R', 'L']:
            raise ValueError(f"'direction' value {direction} is not supported.\nAccepted values are 'R' (right) or 'L' (left).")
        if not which in ['cursor', 'display']:
            raise TypeError(f"'which' value {direction} is not supported.\nMust be either 'cursor' or 'display'.")
        cmd = D4
        if which == 'display':
            cmd |= D3
        if direction == 'R':
            cmd |= D2
        
        self._wr_cmd(cmd)
    
    def function_set(self, data_length:int, display_lines:int, font_type='5x8'):
        if not data_length in [4, 8]:
            raise ValueError(f"'data_length' must be either 4 or 8, not {data_length}.")
        if not display_lines in [1, 2]:
            raise ValueError(f"'display_lines' must be either 1 or 2, not {display_lines}.")
        if not font_type in ['5x8', '5x11']:
            raise ValueError(f"'font_type' must be either '5x8' or '5x11', not {font_type}.")

        cmd = D5
        
        if data_length == 8:
            cmd |= D4
        if display_lines == 2:
            cmd |= D3
        if font_type == '5x11':
            cmd |= D2
        
        self._wr_cmd(cmd)
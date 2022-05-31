import sys
from lcd_i2c import I2CLCD

# I2C INITIALIZATION
lcd = I2CLCD(5, 4, 0x27,4 , 20)

while True:
    try:
        cch = input("Insert data: ")
        lcd.Print(cch)
    except KeyboardInterrupt:
        lcd.exit_handling()
        break
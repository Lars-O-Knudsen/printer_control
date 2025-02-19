# he OLED is indeed a bit weird, you need a bit of trick to get it working: 
# #include <U8g2lib.h> #include <Wire.h> // there is no 72x40 constructor in u8g2 hence the 72x40 screen 
# is mapped in the middle of the 132x64 pixel buffer of the SSD1306 controller 
# U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE, 6, 5); 
# int width = 72; int height = 40; int xOffset = 30; // = (132-w)/2 int yOffset = 12; // = (64-h)/2 
# void setup(void) { 
# delay(1000); 
# u8g2.begin(); u8g2.setContrast(255); // set contrast to maximum 
# u8g2.setBusClock(400000); //400kHz I2C u8g2.setFont(u8g2_font_ncenB10_tr); } 
# void loop(void) { u8g2.clearBuffer(); // clear the internal memory 
# u8g2.drawFrame(xOffset+0, yOffset+0, width, height); //draw a frame around the border 
# u8g2.setCursor(xOffset+15, yOffset+25); 
# u8g2.printf("%dx%d", width, height); 
# u8g2.sendBuffer(); // transfer internal memory to the display }


import machine
import time

# create I2C interface
i2c = machine.SoftI2C( scl=machine.Pin(6),sda=machine.Pin(5),freq=40000) 
print(i2c.scan()) # 0x3c is the I2C address of the SSD1306. As an integer, 60.

# create SSD1306 interface
import ssd1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# turn on all pixels
oled.fill(1) # make the change
oled.show() # show the update
time.sleep(1)
print("start")
oled.fill(0) # make the change
oled.show()
oled.text('Hello, World!', 13, 14, 1)
oled.show()




# ---------------------------------------------------------------------

# from machine import Pin, I2C
# from sh1106 import SH1106_I2C

# WIDTH = 128
# HEIGHT = 64
# X=int((128-70)/2);
# Y=int((64-40)/2);

# # i2c = I2C(0, scl=Pin(6), sda=Pin(5), freq=400000)

# print("I2C Address : "+hex(i2c.scan()[0]).upper())
# print("I2C Configuration: "+str(i2c))

# oled = SH1106_I2C(WIDTH, HEIGHT, i2c)
# oled.rotate(1)
# oled.fill(0)
# oled.contrast(255)
# # oled.text("12345678",12,12)

# oled.text("12345678",X,Y)
# oled.text("ABCDEFGH",X+10,Y+10)
# oled.text("12345678",X+20,Y+20)
# oled.text("ABCDEFGH",X+30,Y+30)
# # oled.text("12345678",40,36)
# # oled.text("12345678",30,45)
# oled.show()

# import time
# from machine import Pin, SoftI2C as I2C
# from sh1106 import SH1106_I2C


# oled: SH1106_I2C = None


# def init_oled():
#     global oled
#     # create I2C interface
#     i2c = I2C( scl=Pin(6),sda=Pin(5),freq=40000) 
#     print(i2c.scan()) # 0x3c is the I2C address of the SSD1306. As an integer, 60.
#     print("I2C Address : "+hex(i2c.scan()[0]).upper())
#     print("I2C Configuration: "+str(i2c))

#     WIDTH = 128
#     HEIGHT = 64
#     X=int((128-70)/2);
#     Y=int((64-40)/2);


#     oled = SH1106_I2C(WIDTH, HEIGHT, i2c)
#     oled.xoffs=X
#     oled.yoffs=Y
#     oled.rotate(1)
#     oled.fill(0)
#     oled.contrast(255)
#     oled.show()
#     log("--INIT--")


def log(txt:str):
    print(txt)
    
# def log(txt:str):
#     oled.write(f"{txt:<8}",0,10)
#     oled.write( time.strftime("%H:%M:%S", time.localtime()) ,0,25)

# def write(s:str, x:int, y:int, reset:bool=False):
#     global oled
#     if reset:
#         oled.fill(0)
#     oled.text(s, oled.xoffs+x, oled.yoffs+y)
#     oled.show()



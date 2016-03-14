from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
import mraa
import pyupm_i2clcd as lcd
from twisted.protocols import basic
from twisted.internet import reactor, protocol

if __name__ == "__main__":
            
    class Grove_LCD(WuClass):
        def __init__(self):
            self.ID = 2010
	    self.myLcd=lcd.Jhd1313m1(0,0x3E,0x62)
            print "LCD Actuator init success"

        def update(self,obj,pID,val):
            value=obj.getProperty(0)##get value's property
            on_off=obj.getProperty(1)##get on_off's property
            red=obj.getProperty(2)##get red's property
            green=obj.getProperty(3)##get green's property 
            blue=obj.getProperty(4)##get blue's property 
            if on_off:
                self.myLcd.setColor( red, green, blue) ##set color
                self.myLcd.setCursor(1,0)##move cursor to 1 row, 0 col
            	self.myLcd.write("Hello ")## print hello
                print "on_off is true\n"
            else:
                self.myLcd.setColor( 0, 0, 0) ##set color
                print "on_off is fail\n"
            print "red:"+str(red)+" green:"+str(green)+" blue:"+str(blue)
            print "\n on_off:"+str(on_off)
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
			
            self.m1 = Grove_LCD()
            self.addClass(self.m1,0)
            self.obj_grove_lcd = self.addObject(self.m1.ID)
				

    if len(sys.argv) <= 2:
        print 'python udpwkpf.py <ip> <port>'
        print '      <ip>: IP of the interface'
        print '      <port>: The unique port number in the interface'
        print ' ex. python udpwkpf.py <gateway IP> <local IP>:3000'
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()

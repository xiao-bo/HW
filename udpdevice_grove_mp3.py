from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
import mraa

from twisted.protocols import basic
from twisted.internet import reactor, protocol

if __name__ == "__main__":
            
    class Grove_MP3(WuClass):
        def __init__(self):
            self.ID = 2011
            print "MP3 Actuator init success"
        def update(self,obj,pID,val):
            if pID == 0:
                if val == True:
                    #self.light_actuator_gpio.write(1)
                    print "MP3 Actuator On"
                else:
                    #self.light_actuator_gpio.write(0)
                    print "MP3 Actuator Off"
            else:
                print "MP3 Actuator error"

    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):

            self.m1 = Grove_MP3()
            self.addClass(self.m1,0)
            self.obj_grove_mp3 = self.addObject(self.m1.ID)
			"""
            self.m2 = Slider()
            self.addClass(self.m2,0)
            self.obj_slider = self.addObject(self.m2.ID)

            self.m3 = Threshold()
            self.addClass(self.m3,1)
            self.obj_threshold = self.addObject(self.m3.ID)
            reactor.callLater(1,self.loop)
			"""
        #def loop(self):
            #self.obj_slider.setProperty(2, self.m2.current_value)
            #reactor.callLater(1,self.loop)

    if len(sys.argv) <= 2:
        print 'python udpwkpf.py <ip> <port>'
        print '      <ip>: IP of the interface'
        print '      <port>: The unique port number in the interface'
        print ' ex. python udpwkpf.py <gateway IP> <local IP>:3000'
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()

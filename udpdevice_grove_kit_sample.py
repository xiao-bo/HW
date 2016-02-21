from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
import mraa

from twisted.protocols import basic
from twisted.internet import reactor, protocol

if __name__ == "__main__":
    class Threshold(WuClass):
        def __init__(self):
            self.ID = 1
            print "Threshold init success"
        def update(self,obj,pID,val):
            print "Threshold input value: ", val
            if pID == 2:
                op = obj.getProperty(0)
                if op == 0:
                    if val < obj.getProperty(1):
                        print "op= ", op, " True"
                        obj.setProperty(3,True)
                    else:
                        print "op= ", op, " False"
                        obj.setProperty(3,False)
                elif op == 1:
                    if val > obj.getProperty(1):
                        print "op= ", op, " True"
                        obj.setProperty(3,True)
                    else:
                        print "op= ", op, " False"
                        obj.setProperty(3,False)
                elif op == 2:
                    if val <= obj.getProperty(1):
                        print "op= ", op, " True"
                        obj.setProperty(3,True)
                    else:
                        print "op= ", op, " False"
                        obj.setProperty(3,False)
                elif op == 3:
                    if val >= obj.getProperty(1):
                        print "op= ", op, " True"
                        obj.setProperty(3,True)
                    else:
                        print "op= ", op, " False"
                        obj.setProperty(3,False)
                else:
                    print "Error: unknown operator %d" % op
            pass
        def init(self):
            pass

    class Slider(WuClass):
        def __init__(self):
            self.ID = 1006
            self.slider_aio = mraa.Aio(0)
            self.current_value = 0
            print "Slider init success"
            reactor.callLater(0.5, self.refresh)
        def update(self,obj,pID,val):
            pass
        def refresh(self):
            self.current_value = self.slider_aio.read()
            print "Slider value: ", self.current_value
            reactor.callLater(0.5, self.refresh)
            
    class Light_Actuator(WuClass):
        def __init__(self):
            self.ID = 2001
            self.light_actuator_gpio = mraa.Gpio(2)
            self.light_actuator_gpio.dir(mraa.DIR_OUT)
            print "Light Actuator init success"
        def update(self,obj,pID,val):
            if pID == 0:
                if val == True:
                    self.light_actuator_gpio.write(1)
                    print "Light Actuator On"
                else:
                    self.light_actuator_gpio.write(0)
                    print "Light Actuator Off"
            else:
                print "Light Actuator garbage"

    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):

            self.m1 = Light_Actuator()
            self.addClass(self.m1,0)
            self.obj_light_actuator = self.addObject(self.m1.ID)

            self.m2 = Slider()
            self.addClass(self.m2,0)
            self.obj_slider = self.addObject(self.m2.ID)

            self.m3 = Threshold()
            self.addClass(self.m3,1)
            self.obj_threshold = self.addObject(self.m3.ID)
            reactor.callLater(1,self.loop)

        def loop(self):
            self.obj_slider.setProperty(2, self.m2.current_value)
            reactor.callLater(1,self.loop)

    if len(sys.argv) <= 2:
        print 'python udpwkpf.py <ip> <port>'
        print '      <ip>: IP of the interface'
        print '      <port>: The unique port number in the interface'
        print ' ex. python udpwkpf.py <gateway IP> <local IP>:3000'
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()

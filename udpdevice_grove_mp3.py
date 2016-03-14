from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
import mraa
import pyupm_wt5001 as upmWt5001

from twisted.protocols import basic
from twisted.internet import reactor, protocol

if __name__ == "__main__":

    class Grove_MP3(WuClass):
        def __init__(self):
            self.ID = 2011
            self.myMP3Player = upmWt5001.WT5001(0)
            print "MP3 Actuator init success"
        def update(self,obj,pID,val):
	    ##get current play state 
	    ps = upmWt5001.uint8Array(0)
	    self.myMP3Player.getPlayState(ps)
				
	    on_off=obj.getProperty(0)##get on_off's property 
	    track=obj.getProperty(1)##get track's property 
            if on_off:
                if ps:
		    self.myMP3Player.play(upmWt5001.WT5001.SD, track)
                    print "playing \n"
                else:
                    print "ps is fail\n"
            else:
                print "on_off is fail\n"

            print "track:"+str(track)
            print "on_off:"+str(on_off)

    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
			
            self.m1 = Grove_MP3()
            self.addClass(self.m1,0)
            self.obj_grove_mp3 = self.addObject(self.m1.ID)
				

    if len(sys.argv) <= 2:
        print 'python udpwkpf.py <ip> <port>'
        print '      <ip>: IP of the interface'
        print '      <port>: The unique port number in the interface'
        print ' ex. python udpwkpf.py <gateway IP> <local IP>:3000'
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()

import sys
import mraa
import time
from hbridge_sparkfun_tb6612 import HBridge_SparkFun_TB6612

class Car(object):
    def __init__(self):
        self.h_ridge = HBridge_SparkFun_TB6612()
        self.h_ridge.disable_motors(False)

        # B
        self._enB = mraa.Gpio(5)
        self._enB.dir(mraa.DIR_OUT)

        self._dirB0 = mraa.Gpio(6)
        self._dirB0.dir(mraa.DIR_OUT)

        self._dirB1 = mraa.Gpio(7)
        self._dirB1.dir(mraa.DIR_OUT)

    def enable_en(self):
        print 'enable Car'
        self._enA.write(1)
        self._enB.write(1)

    def disable_en(self):
        self._enA.write(0)
        self._enB.write(0)


    def back(self):
        self._dirA0.write(0)
        self._dirA1.write(1)

        self._dirB0.write(0)
        self._dirB1.write(1)

    def forward(self):
        self._dirA0.write(1)
        self._dirA1.write(0)

        self._dirB0.write(1)
        self._dirB1.write(0)

    def _get_dir(self):
        if self._dirA0.read() == 1 and self._dirA1.read() == 0 and self._dirB0.read() == 1 and self._dirB1.read() == 0:
            return 'forward'
        if self._dirA0.read() == 0 and self._dirA1.read() == 1 and self._dirB0.read() == 0 and self._dirB1.read() == 1:
            return 'backward'
        return 'stop'




    def turn_left(self,angle=0):
        print "turn left"

        dir = self._get_dir()
        self._dirA0.write(1)
        self._dirA1.write(0)

        self._dirB0.write(0)
        self._dirB1.write(1)
        time.sleep(0.1)
        if dir == 'forward':
            self.forward()
        elif dir == 'backward':
            self.back()
        else:
            self.stop()

    def turn_right(self,angle=0):
        print "turn right"
        dir = self._get_dir()
        self._dirA0.write(0)
        self._dirA1.write(1)

        self._dirB0.write(1)
        self._dirB1.write(0)
        time.sleep(0.1)
        if dir == 'forward':
            self.forward()
        elif dir == 'backward':
            self.back()
        else:
            self.stop()

    def stop(self):
        print "stop"
        self._dirA0.write(1)
        self._dirA1.write(1)

        self._dirB0.write(1)
        self._dirB1.write(1)

    def going_to_stop(self):
        print "going to stop"
        self._dirA0.write(0)
        self._dirA1.write(0)

        self._dirB0.write(0)
        self._dirB1.write(0)

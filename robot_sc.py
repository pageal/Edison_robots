#https://github.com/sparkfun/SparkFun_H-Bridge_Block_for_Edison_CPP_Library/blo$
#http://www.i-programmer.info/programming/hardware/8744-exploring-edison-mraa-g$
#https://github.com/intel-iot-devkit/mraa/tree/master/examples/python

import mraa
print("mraa imported")

import time



#mraa pins
PWMA=20 #PWM0, which is pin 20 in mraa
PWMB=14 #PWM1, which is pin 14 in mraa
AIN1=33 #GPIO48, which is pin 33 in mraa
AIN2=46 #GPIO47, which is pin 46 in mraa
STBY=47 #GPIO49, which is pin 47 in mraa
BIN1=48 #GPIO15, which is pin 48 in mraa
BIN2=36 #GPIO14, which is pin 36 in mraa

pwma = mraa.Pwm(PWMA)
pwma.period_us(1000)
pwma.enable(True)

pwmb = mraa.Pwm(PWMB)
pwmb.period_us(1000)
pwmb.enable(True)

pwma.write(0.01)
pwmb.write(0.01)
pwma.write(0.0)
pwmb.write(0.0)

a1 = mraa.Gpio(AIN1)
a1.dir(mraa.DIR_OUT)
a1.mode(mraa.MODE_STRONG)

a2 = mraa.Gpio(AIN2)
a2.dir(mraa.DIR_OUT)
a1.mode(mraa.MODE_STRONG)

a2 = mraa.Gpio(AIN2)
a2.dir(mraa.DIR_OUT)
a2.mode(mraa.MODE_STRONG)

b1 = mraa.Gpio(BIN1)
b1.dir(mraa.DIR_OUT)
b1.mode(mraa.MODE_STRONG)

b2 = mraa.Gpio(BIN2)
b2.dir(mraa.DIR_OUT)
b2.mode(mraa.MODE_STRONG)

sb = mraa.Gpio(STBY)
sb.dir(mraa.DIR_OUT)
sb.mode(mraa.MODE_STRONG)
sb.write(1)

def move(xpa,xpb,xa1,xa2,xb1,xb2):
#       time.sleep(0.1)
        pwma.write(xpa)
        pwmb.write(xpb)
        a1.write(xa1)
        b1.write(xb1)
        a2.write(xa2)
        b2.write(xb2)
#        time.sleep(0.1)

def stop():
        a1.write(0)
        b1.write(0)
        a2.write(0)
        b2.write(0)

def forward():
        print("fwd")
        move(1,1,1,0,1,0)

def back():
        print("bkw")
        move(1,1,0,1,0,1)

def lrotate():
        move(1,1,0,1,1,0)

def rrotate():
        move(1,1,1,0,0,1)

def lturn():
        move(0.5,1,1,0,1,0)

def rturn():
        move(1,0.5,1,0,1,0)


#stop()
#time.sleep(5)
forward()
time.sleep(5)
time.sleep(5)
back()
time.sleep(5)
stop()


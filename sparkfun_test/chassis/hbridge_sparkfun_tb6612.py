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

class HBridge_SparkFun_TB6612():
    def __init__(self):
        self._dca = 0.0
        self._dcb = 0.0

        self._pwma = mraa.Pwm(PWMA)
        self._pwma.period_us(1000)
        self._pwma.enable(True)

        self._pwmb = mraa.Pwm(PWMB)
        self._pwmb.period_us(1000)
        self._pwmb.enable(True)

        self._pwma.write(0.01)
        self._pwmb.write(0.01)
        self._pwma.write(0.0)
        self._pwmb.write(0.0)

        self._a1 = self.init_gpio(AIN1)
        self._a2 = self.init_gpio(AIN2)
        self._b1 = self.init_gpio(BIN1)
        self._b2 = self.init_gpio(BIN2)
        self._sb = self.init_gpio(STBY)

    def init_gpio(self, pin):
        pin_obj = mraa.Gpio(pin)
        pin_obj.dir(mraa.DIR_OUT)
        pin_obj.mode(mraa.MODE_STRONG)
        pin_obj.write(1)
        return pin_obj

    def disable_motors(self, disable = True):
        stby = 0
        if(disable == False): stby = 1
        self._sb.write(stby)

    def drive(self, dca, dcb):
      self._dca=dca;
      self._dcb=dcb;
      if (dca < 0):
        self.rev_a()
        dca *= -1;
      else:
        self.fwd_a()

      if (dcb < 0):
        self.rev_b()
        dcb *= -1;
      else:
        self.fwd_b()

      self._pwma.write(dca)
      self._pwmb.write(dcb)

    def brake(self, brake_a, brake_b):
      if (brake_a):
        self._a1.write(1)
        self._a2.write(1)
      if (brake_b):
        self._b1.write(1)
        self._b2.write(1)

    def fwd_a(self):
      self._a1.write(0)
      self._a2.write(1)

    def rev_a(self):
      self._a1.write(1)
      self._a2.write(0)

    def fwd_b(self):
      self._b1.write(0)
      self._b2.write(1)

    def rev_b(self):
      self._b1.write(1)
      self._b2.write(0)


    '''
    bool tb6612::getStandby()
    {
      if (mraa_gpio_read(_standbyPin) == 0)
      {
        return true;
      }
      else
      {
        return false;
      }
    }

    void tb6612::getDiffDrive(float* dcA, float* dcB)
    {
      *dcA = _dcA;
      *dcB = _dcB;
    }

    void tb6612::getShortBrake(bool* brakeA, bool* brakeB)
    {
      if ( (mraa_gpio_read(_A1) == 1) && (mraa_gpio_read(_A2) == 1) )
      {
        *brakeA = true;
      }
      else
      {
        *brakeA = false;
      }
      if ( (mraa_gpio_read(_B1) == 1) && (mraa_gpio_read(_B2) == 1) )
      {
        *brakeB = true;
      }
      else
      {
        *brakeB = false;
      }
    }
    '''

def test():
  # The constructor for the tb6612 class object configures all the necessary
  # pins, exporting them if they aren't already exported, etc. Note that only
  #  one tb6612 class object may exist at a time, as they share hardware
  #  resources!
  motors = HBridge_SparkFun_TB6612()

  # The constructor disables the outputs of the tb6612 by asserting the standby
  #  pin on the controller. You *must* use the disable_motors() function to enable
  #  them before proceeding!
  motors.disable_motors(False)

  # drive() accepts a floating point number for channel A and channel B, in
  #  the range -1.0 to 1.0 inclusive.
  print("fwd")
  motors.drive(0.5,0.5);
  time.sleep(5);

  print("rev")
  motors.drive(-0.5,-0.5);
  time.sleep(5);

  # "short brake" literally means the two outputs are shorted together. This
  #  drags the motor to a halt in a very short time and then holds it still
  #  (albeit fairly weakly). The shortBrake() function doesn't change the
  #  PWM output settings, so when shortBrake() is released by sending a "false"
  #  parameter, the motor will immediately resume its previous speed.
  motors.brake(True, True);

  # Return the motors to hi-z state. This also doesn't affect the PWM output,
  #  so when standby is released (by passing false to this function) the motors
  #  will immediately resume their former speeds. This also doesn't provide any
  #  braking, so the motors will coast to a stop much more slowly than with
  #  shortBrake().
  motors.disable_motors();

  '''
  bool brakeA = false;
  bool brakeB = false;
  float dcA = 0;
  float dcB = 0;
  bool onStandby = false;

  // We've provided a number of "get" functions, to check the current
status of
  //  the device.

  // getStandby() returns true if the motors are on standby, false
otherwise.
  //  This function checks the actual status of the gpio pin used for
setting
  //  the standby mode on the chip, so it will always match reality.
  onStandby = motors.getStandby();

  // getDiffDrive() checks the *stored* speed value, rather than the
current
  //  value. Thus, if another process alters the PWM output duty cycle
without
  //  actually touching the class object, this may return invalid data.
It also
  //  doesn't return any information about standby or brake status.
  motors.getDiffDrive(&dcA, &dcB);

  // getShortBrake() checks the pins used for setting the
direction/brake mode,
  //  so the values placed into the pointer parameters by the function
are
  //  accurate at the time the function is called.
  motors.getShortBrake(&brakeA, &brakeB);

  cout<<"Motor standby status: "<< boolalpha << onStandby << endl;
  cout<<"Motor A brake status: "<< brakeA << endl;
  cout<<"Motor B brake status: "<< brakeB << endl;
  cout<<"Channel A speed: "<< fixed << setprecision(3)<<dcA<<endl;
  cout<<"Channel B speed: "<<dcB<<endl;

  return 0;
  '''

#test()




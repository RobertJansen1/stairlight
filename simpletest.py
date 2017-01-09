# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
from subprocess import call

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

# Configure min and max servo pulse lengths
servo_min = 1050  # Min pulse length out of 4096
servo_max = 4095  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
# pick something between 24 and 1526hz
pwm.set_pwm_freq(1524)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    step = range(0,4000,5)
    #step=step[0::3]
    for i in (step):
      f=str(i)
      #print i
      pwm.set_pwm(15,0,i)
    for i in (step):
      f=str(i)
      #print i
      pwm.set_pwm(14,0,i)
    for i in (step):
      f=str(i)
      #print i
      pwm.set_pwm(12,0,i)
    for i in (step):
      f=str(i)
      #print i
      pwm.set_pwm(11,0,i)
    for i in (step):
      f=str(i)
      #print i
      pwm.set_pwm(10,0,i)

    # Move servo on channel O between extremes.
    #pwm.set_pwm(15, 0, 0)
    time.sleep(.5)
    #pwm.set_pwm(15, 0, 500)
    #time.sleep(.5)
    #pwm.set_pwm(15, 0, 1500)
    #time.sleep(.5)
    #pwm.set_pwm(15, 0, 3000)
    #time.sleep(.5)

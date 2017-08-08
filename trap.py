#!/usr/bin/python

# -----------------------
# Import required Python libraries
# -----------------------
from __future__ import division
import time
from datetime import datetime
import logging
from multiprocessing import Process
import threading
import subprocess
from subprocess import call
from subprocess import check_output
import RPi.GPIO as GPIO
# Import the PCA9685 module.
import Adafruit_PCA9685

# -----------------------
# Setting variables
# -----------------------

from variables import *
# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='/run/shm/trap.log',level=logging.INFO)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIRB_PIN, GPIO.IN)
GPIO.setup(PIRT_PIN, GPIO.IN)

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
red   = Adafruit_PCA9685.PCA9685(address=0x48, busnum=1)
green = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
blue  = Adafruit_PCA9685.PCA9685(address=0x50, busnum=1)
white = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)

# Set frequency to 60hz, good for servos.
# pick something between 24 and 1526hz
red.set_pwm_freq(1000)
blue.set_pwm_freq(1000)
green.set_pwm_freq(1000)
white.set_pwm_freq(1000)

# Configure min and max servo pulse lengths
servo_min = 1050  # Min pulse length out of 4096
servo_max = 4095  # Max pulse length out of 4096
# -----------------------
# Define some functions
# -----------------------

# non_used? Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def fadenew(trede, color, src, dest, stepsize, delay=0):
  #printing vars
  #print trede
  #print color
  #print int(src)
  #print int(dest)
  #print int(stepsize)
  if color == "red":
    pwm = red
  if color == "blue":
    pwm = blue
  if color == "green":
    pwm = green
  else:
    #fallback to white
    pwm = white
  if src < dest:
    stepsize = -stepsize
  step = range(int(src),int(dest),int(stepsize))
  for i in (step):
    #print "setting "+str(trede)+" to "+str(i)
    pwm.set_pwm(int(trede), 0, int(i))
    time.sleep(delay)

def fade(trede, direction, step, delay=0):
  if direction == 'on':
    val = 0
    #int(check_output(["pigs", "gdc " + trede]))
    step = range(val,step,stepsize)
    for i in (step):
      f=int(i)
      trede=int(trede)
      #print i
      #red.set_pwm(i, 0, 0)
      #blue.set_pwm(i, 0, 0)
      white.set_pwm(trede, 0, i)
      #green.set_pwm(i, 0, 0)
      time.sleep(delay)
  else:
    val = valw
    #int(check_output(["pigs", "gdc " + trede]))
    step = range (val,0,-stepsize)
    #step=-step
    for i in (step) + [0]:
      f=int(i)
      trede=int(trede)
      #print i
      white.set_pwm(trede, 0, i)
      #call(["pigs", "p "+trede+" "+f])
      time.sleep(delay)

def fix(state):
  print 'applying temporary gpio fix'
  if state == 'off':
    for signal in (4,5,6,7,8,9,10,11,13,15,17,18,19):
      calc = 0
      value = str(calc + 1)
      channel = str(signal)
      call(["pigs", "p "+channel+" "+value])
      time.sleep(ndel)
      value = str(calc)
      call(["pigs", "p "+channel+" "+value])
      time.sleep(ndel)
  if state == 'on':
    for signal in (4,5,6,7,8,9,10,11,13,15,17,18,19):
      calc = valw
      value = str(calc + 1)
      channel = str(signal)
      call(["pigs", "p "+channel+" "+value])
      time.sleep(ndel)
      value = str(calc)
      call(["pigs", "p "+channel+" "+value])
      time.sleep(ndel)

def up_to_down():
  # This function starts the leds from up to down
  print "activating boven naar beneden"
  threads = []
  for trede in (range(1,14)):
    threads.append(threading.Thread(target=fadenew, args=(trede, 'white', '0', valw, stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'red', '0', valr, stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'blue', '0', valb, stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'green', '0', valg, stepsize)))

  for thread in reversed(threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();


  #fix('on')
  #fade(rgbr, 'on', valr)
  #fade(rgbg, 'on', valg)
  #fade(rgbb, 'on', valb)

  delay = time.time() + timeout
  while time.time() < delay:
    if GPIO.input(PIRT_PIN):
      print "1 extra persoon restarting timer"
      delay = time.time() + timeout
    else:
      print "nobody on tree13"
      if GPIO.input(PIRB_PIN):
        print "ending loop"
        delay = time.time() + wait + wait + wait
      else:
        remaining = delay - time.time()
        print "not there yet " + str(remaining) + " seconds remaining"
    time.sleep(wait)
  print "done"

def down_to_up():
  # This function starts the leds from down to up
  print "activating beneden naar boven"
  threads = []
  for trede in (range(1,14)):
    threads.append(threading.Thread(target=fadenew, args=(trede, 'white', '0', valw, stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'red', '0', valr, stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'blue', '0', valb, stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'green', '0', valg, stepsize)))

  for thread in (threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();

  #fix('on')
  #fade(rgbr, 'on', valr)
  #fade(rgbg, 'on', valg)
  #fade(rgbb, 'on', valb)

  delay = time.time() + timeout
  count = 1
  while time.time() < delay:
    if GPIO.input(PIRB_PIN):
      print "1 extra persoon restarting timer"
      delay = time.time() + timeout
    else:
      print "nobody on tree1"
      if GPIO.input(PIRT_PIN):
        print "ending loop"
        delay = time.time() + wait + wait + wait
      else:
        remaining = delay - time.time()
        print "not there yet " + str(remaining) + " seconds remaining"
    time.sleep(wait)
  print "done"

def shutdown_to_up():
  print "deactivating beneden naar boven"
  threads = []
  for trede in (range(1,14)):
    threads.append(threading.Thread(target=fadenew, args=(trede, 'white', valw, '0', stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'red', valr, '0', stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'blue', valb, '0', stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'green', valg, '0', stepsize)))

  for thread in (threads):
    thread.start()
    time.sleep(ndel)
  time.sleep(5)

  for thread in threads:
    thread.join();
  #fix('off')
  #fade(rgbr, 'off', valr)
  #fade(rgbg, 'off', valg)
  #fade(rgbb, 'off', valb)
  
def shutup_to_down():
  print "deactivating boven naar beneden"
  threads = []
  for trede in (range(1,14)):
    threads.append(threading.Thread(target=fadenew, args=(trede, 'white', valw, '0', stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'red', valr, '0', stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'blue', valb, '0', stepsize)))
    threads.append(threading.Thread(target=fadenew, args=(trede, 'green', valg, '0', stepsize)))

  for thread in reversed(threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();
  #fix('off')
  time.sleep(5)
  #fade(rgbr, 'off', valr)
  #fade(rgbg, 'off', valg)
  #fade(rgbb, 'off', valb)

def killshutdown():
  print "Detected motion, killing shutdown"
  pshut.terminate()

# -----------------------
# Main Script
# -----------------------

print "Motion Detection"

try:
  while True:
    if GPIO.input(PIRT_PIN):
      print "triggered motion top"
      logging.info('triggered motion top')
      up_to_down()
      pshut = Process(target=shutup_to_down, args=())
      pshut.start()
      while pshut.is_alive():
        if GPIO.input(PIRB_PIN):
          killshutdown()
        if GPIO.input(PIRT_PIN):
          killshutdown()
        print "no motion noticed while shutting down"
        time.sleep(wait)
    if GPIO.input(PIRB_PIN):
      print "kleiner"
      logging.info('triggered motion bottom')
      down_to_up()
      pshut = Process(target=shutdown_to_up, args=())
      pshut.start()
      while pshut.is_alive():
        if GPIO.input(PIRB_PIN):
          killshutdown()
        if GPIO.input(PIRT_PIN):
          killshutdown()
        print "no motion noticed while shutting down"
        time.sleep(wait)
    logging.info('no motion noticed')
    time.sleep(wait)

except KeyboardInterrupt:
  # User pressed CTRL-C
  print "Done"

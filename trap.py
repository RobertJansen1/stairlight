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
pwm_freq = 1524
red.set_pwm_freq(150)
blue.set_pwm_freq(150)
green.set_pwm_freq(150)
white.set_pwm_freq(150)


def fadenew(trede, color, src, dest, stepsize, delay=0):
  if color == "red":
    pwm = red
  elif color == "blue":
    pwm = blue
  elif color == "green":
    pwm = green
  else:
    #fallback to white
    pwm = white
  if int(src) < int(dest):
    stepsize = -stepsize
  step = range(int(src),int(dest),int(stepsize))
  for i in (step):
    #print "setting "+str(trede)+" to "+str(i)
    pwm.set_pwm(int(trede), 0, int(i))
    time.sleep(delay)
  pwm.set_pwm(int(trede), 0, int(dest))
  


def up_to_down():
  # This function starts the leds from up to down
  print "activating boven naar beneden"
  threads = []
  for trede in valgreen.keys():
    for color in ('red','blue','green','white'):
      if color == "red":
        values = valred
      elif color == "blue":
        values = valblue
      elif color == "green":
        values = valgreen
      else:
        values = valwhite
      threads.append(threading.Thread(target=fadenew, args=(trede, color, '0', values[trede], stepsize)))

  for thread in reversed(threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();

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
  for trede in valgreen.keys():
    for color in ('white','red','blue','green'):
      if color == "red":
        values = valred
      elif color == "blue":
        values = valblue
      elif color == "green":
        values = valgreen
      else:
        values = valwhite
      threads.append(threading.Thread(target=fadenew, args=(trede, color, '0', values[trede], stepsize)))

  for thread in (threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();

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
  for trede in valgreen.keys():
    for color in ('white','red','blue','green'):
      if color == "red":
        values = valred
      elif color == "blue":
        values = valblue
      elif color == "green":
        values = valgreen
      else:
        values = valwhite
      threads.append(threading.Thread(target=fadenew, args=(trede, color, values[trede], '0', stepsize)))

  for thread in (threads):
    thread.start()
    time.sleep(ndel)
#  time.sleep(5)

  for thread in threads:
    thread.join();
  
def shutup_to_down():
  print "deactivating boven naar beneden"
  threads = []
  for trede in valgreen.keys():
    for color in ('white','red','blue','green'):
      if color == "red":
        values = valred
      elif color == "blue":
        values = valblue
      elif color == "green":
        values = valgreen
      else:
        values = valwhite
      threads.append(threading.Thread(target=fadenew, args=(trede, color, values[trede], '0', stepsize)))

  for thread in reversed(threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();
#  time.sleep(5)

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
#      while pshut.is_alive():
#        if GPIO.input(PIRB_PIN):
#          killshutdown()
#        if GPIO.input(PIRT_PIN):
#          killshutdown()
#        print "no motion noticed while shutting down"
#        logging.debug('no motion noticed while shutting down')
#        time.sleep(wait)
    if GPIO.input(PIRB_PIN):
      print "kleiner"
      logging.info('triggered motion bottom')
      down_to_up()
      pshut = Process(target=shutdown_to_up, args=())
      pshut.start()
#      while pshut.is_alive():
#        if GPIO.input(PIRB_PIN):
#          killshutdown()
#        if GPIO.input(PIRT_PIN):
#          killshutdown()
#        print "no motion noticed while shutting down"
#        logging.debug('no motion noticed while shutting down')
#        time.sleep(wait)
    logging.debug('no motion noticed')
    time.sleep(wait)

except KeyboardInterrupt:
  # User pressed CTRL-C
  print "Done"

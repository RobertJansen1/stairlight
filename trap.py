#!/usr/bin/python

# -----------------------
# Import required Python libraries
# -----------------------
from __future__ import division
import time
from datetime import datetime
from astral import Astral
import datetime
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

#setting proper GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIRB_PIN, GPIO.IN)
GPIO.setup(PIRT_PIN, GPIO.IN)

# Setting the addresses for the PCA chips
red   = Adafruit_PCA9685.PCA9685(address=0x48, busnum=1)
green = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
blue  = Adafruit_PCA9685.PCA9685(address=0x50, busnum=1)
white = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)

# Set frequency to 150hz, good for servos.
# pick something between 24 and 1526hz
red.set_pwm_freq(150)
blue.set_pwm_freq(150)
green.set_pwm_freq(150)
white.set_pwm_freq(150)

def set_color1():
  global valwhite
  global valred
  global valblue
  global valgreen
  valwhite = {}
  for trede in (range(1,14)):
    valwhite[trede] = 201
  valred = {
    1: 500,
    2: 0,
    3: 500,
    4: 0,
    5: 0,
    6: 500,
    7: 0,
    8: 0,
    9: 500,
    10: 0,
    11: 0,
    12: 500,
    13: 0,
  }
  valblue = {
    1: 0,
    2: 500,
    3: 0,
    4: 0,
    5: 500,
    6: 0,
    7: 0,
    8: 500,
    9: 0,
    10: 0,
    11: 500,
    12: 0,
    13: 0,
  }
  valgreen = {
    1: 500,
    2: 0,
    3: 0,
    4: 500,
    5: 0,
    6: 0,
    7: 500,
    8: 0,
    9: 0,
    10: 500,
    11: 0,
    12: 0,
    13: 500,
  }

def set_color2():
  global valwhite
  global valred
  global valblue
  global valgreen
  valwhite = {}
  valred = {}
  valblue = {}
  valgreen = {}
  for trede in (range(1,14)):
    valwhite[trede] = 101
  for trede in (range(1,14)):
    valblue[trede] = 0
  for trede in (range(1,14)):
    valgreen[trede] = 0
  for trede in (range(1,14)):
    valred[trede] = 20

def set_timezone_vars():
  city_name = 'Amsterdam'
  
  a = Astral()
  a.solar_depression = 'civil'
  
  city = a[city_name]
  global sun
  global timezone
  
  #print('Information for %s/%s\n' % (city_name, city.region))
  
  timezone = city.timezone
  #print('Timezone: %s' % timezone)
  
  #print('Latitude: %.02f; Longitude: %.02f\n' % \
  #    (city.latitude, city.longitude))
  sun = city.sun(date=datetime.datetime.now(), local=True)
  timezone = sun['dawn'].tzinfo

def set_light_vars():
  #set current date to variable
  global date
  date = datetime.datetime.now(timezone)
  if sun['dawn'] <= date <= sun['sunrise']:
    print 'schemer'
    set_color1()
  elif sun['sunrise'] <= date <= sun['noon']:
    print 'ochtend'
    set_color1()
    print valred
    print valblue
  elif sun['noon'] <= date <= sun['sunset']:
    print 'middag'
    set_color1()
  elif sun['sunset'] <= date <= sun['dusk']:
    print 'avondschemer'
    set_color1()
  else: 
    set_color2()
    print 'nacht'


def fadenew(trede, color, src, dest, stepsize, delay=0.01):
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

  if date.day != sun['sunset'].day:
    print "changing date"
    set_timezone_vars()

  for thread in threads:
    thread.join();

#  time.sleep(5)

def killshutdown():
  print "Detected motion, killing shutdown"
  pshut.terminate()

# -----------------------
# Main Script
# -----------------------

# Setting timezone variables
set_timezone_vars()

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
        logging.debug('no motion noticed while shutting down')
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
        logging.debug('no motion noticed while shutting down')
        time.sleep(wait)
    logging.debug('no motion noticed')
    set_light_vars()
    time.sleep(wait)

except KeyboardInterrupt:
  # User pressed CTRL-C
  print "Done"

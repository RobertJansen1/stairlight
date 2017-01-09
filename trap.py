#!/usr/bin/python

# -----------------------
# Setting variables
# -----------------------
timeout = 20
wait = .3
ndel = .1
fdel = .01
treetimeout = 0
stepsize = 1
# -----------------------
# Import required Python libraries
# -----------------------
import time
from datetime import datetime
import logging
#from subprocess import *
from multiprocessing import Process

import subprocess
from subprocess import call
from subprocess import check_output
from variables import *
import RPi.GPIO as GPIO
logging.basicConfig(filename='/run/shm/trap.log',level=logging.INFO)

GPIO.setmode(GPIO.BCM)
PIRB_PIN = 0
PIRT_PIN = 1
GPIO.setup(PIRB_PIN, GPIO.IN)
GPIO.setup(PIRT_PIN, GPIO.IN)

# -----------------------
# Define some functions
# -----------------------
def fade(trede, direction, step, delay=0):
  if direction == 'on':
    val = int(check_output(["pigs", "gdc " + trede]))
    step = range(val,step,stepsize)
    #step=step[0::3]
    for i in (step):
      f=str(i)
      #print i
      call(["pigs", "p "+trede+" "+f])
      time.sleep(delay)
  else:
    val = int(check_output(["pigs", "gdc " + trede]))
    step = range (val,0,-stepsize)
    #step=-step
    for i in (step) + [0]:
      f=str(i)
      #print i
      call(["pigs", "p "+trede+" "+f])
      time.sleep(delay)

def fix(state):
  if state == 'off':
    for signal in (4,5,6,7,8,9,10,11,13,15,17,18,19):
      calc = 0
      value = str(calc + 1)
      channel = str(signal)
      print 'applying off fix'
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
      print 'applying on fix'
      call(["pigs", "p "+channel+" "+value])
      time.sleep(ndel)
      value = str(calc)
      call(["pigs", "p "+channel+" "+value])
      time.sleep(ndel)

def up_to_down():
  # This function starts the leds from down to up
  print "activating boven naar beneden"
  threads = []
  threads.append(threading.Thread(target=fade, args=(tree1w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree2w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree3w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree4w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree5w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree6w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree7w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree8w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree9w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree10w, 'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree11w, 'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree12w, 'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree13w, 'on', valw)))

  for thread in reversed(threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();


  fix('on')
  fade(rgbr, 'on', valr)
  fade(rgbg, 'on', valg)
  fade(rgbb, 'on', valb)

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
        print "not there yet"
    time.sleep(wait)
  print "done"

def down_to_up():
  # This function starts the leds from down to up
  print "activating beneden naar boven"
  threads = []
  threads.append(threading.Thread(target=fade, args=(tree1w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree2w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree3w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree4w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree5w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree6w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree7w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree8w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree9w,  'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree10w, 'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree11w, 'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree12w, 'on', valw)))
  threads.append(threading.Thread(target=fade, args=(tree13w, 'on', valw)))

  for thread in (threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();

  fix('on')
  fade(rgbr, 'on', valr)
  fade(rgbg, 'on', valg)
  fade(rgbb, 'on', valb)

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
        print "not there yet"
    time.sleep(wait)
  print "done"

def shutdown_to_up():
  print "deactivating beneden naar boven"
  threads = []
  threads.append(threading.Thread(target=fade, args=(tree1w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree2w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree3w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree4w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree5w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree6w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree7w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree8w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree9w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree10w, 'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree11w, 'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree12w, 'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree13w, 'off', valw)))

  for thread in (threads):
    thread.start()
    time.sleep(ndel)
  time.sleep(5)

  for thread in threads:
    thread.join();
  fix('off')
  fade(rgbr, 'off', valr)
  fade(rgbg, 'off', valg)
  fade(rgbb, 'off', valb)
  
def shutup_to_down():
  print "deactivating boven naar beneden"
  threads = []
  threads.append(threading.Thread(target=fade, args=(tree1w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree2w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree3w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree4w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree5w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree6w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree7w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree8w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree9w,  'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree10w, 'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree11w, 'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree12w, 'off', valw)))
  threads.append(threading.Thread(target=fade, args=(tree13w, 'off', valw)))

  for thread in reversed(threads):
    thread.start()
    time.sleep(ndel)

  for thread in threads:
    thread.join();
  fix('off')
  time.sleep(5)
  fade(rgbr, 'off', valr)
  fade(rgbg, 'off', valg)
  fade(rgbb, 'off', valb)

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

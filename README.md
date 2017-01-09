# stairlight
code to allow ledstrips to fade in and out on movement on the stairs

first of all, the video! https://www.youtube.com/watch?v=OHU5veO76uQ
## Setup

1. attach ledtrips to stair steps
1. conenct ledstrips to raspberry pi using breadboard, resistors, TIP120, jumpercables (or soldering) 
1. connect the HC-SR05 PiR sensors to the raspberry pi
1. adjust gpio ports and prefered colors in variables.py
1. install scripts
1. add check.sh to crontab
1. walk down the stairs (or up if you are coding in the basement)

### Software Requirements:
+ python 2.7
+ pigpiod pigs (http://abyz.co.uk/rpi/pigpio/pigs.html)
+ a lot of thigs i probably forgot

### Hardware Requirements:

+ Stairs
+ 5050 RGBWW Led Strip
+ Cables
+ Raspberry pi
+ Breadboard
+ 2x HC-SR05 PIR sensor
+ 1-4 TIP120 Transistor
+ 4x CA9685-16-Channel-12-bit-PWM
+ some resistors
+ more cables

### Wiring
connect the ledstrips to your raspberry like the tutorial here: http://popoklopsi.github.io/RaspberryPi-LedStrip/#!/
i did this seperate for ever step
To be expanded later

### Explanation

the trap.py script uses the HC-SR05 sensors to detect motion on the bottom and top stair steps. when motion is detected, the light will fade in from the corresponding direction. after reaching the other side of the stairs, the light will fade out in the same direction giving a smooth experience.

the check.sh script is added to crontab to check if the script is still running, and restart all if needed.

### to be added

individual color for every stair step

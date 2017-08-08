#!/bin/bash
DIFF=$(diff  /run/shm/trap.log  /run/shm/trapdiff.log) 
if [ "$DIFF" != "" ] 
then
    #echo "The file was modified"
    mv /run/shm/new.log /run/shm/old.log
    grep triggered /run/shm/trap.log > /run/shm/new.log
    diff /run/shm/old.log /run/shm/new.log
    rm -f  /run/shm/trapdiff.log
    touch /run/shm/trap.log
    cp  /run/shm/trap.log  /run/shm/trapdiff.log
else
    echo "Het trap-script is opnieuw afgetrapt."
    rm -f  /run/shm/trap.log
    rm -f  /run/shm/trapdiff.log
    pkill -f pigpiod
    pkill -f trap.py
    touch  /run/shm/trap.log
    touch  /run/shm/trapdiff.log
    sleep 2
    pigpiod -a1
    sleep 2
    nohup python /opt/stairlight/trap.py > /dev/null & 
fi
DIFF2=$(diff /opt/trap/variables.py /opt/trap/diffvariables.py)
if [ "$DIFF2" != "" ]
then
    echo "Het trap-script is opnieuw afgetrapt.(variables)"
    cp /opt/stairlight/variables.py /opt/stairlight/diffvariables.py
    rm -f  /run/shm/trap.log
    rm -f  /run/shm/trapdiff.log
    pkill -f pigpiod
    pkill -f trap.py
    touch  /run/shm/trap.log
    touch  /run/shm/trapdiff.log
    sleep 2
    pigpiod -a1
    sleep 2
    nohup python /opt/stairlight/trap.py > /dev/null &
fi

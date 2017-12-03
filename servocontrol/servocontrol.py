#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys, getopt



def rotate_servo(degree):
    servoPIN = 17
    min = 2.5
    max = 12.6
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 als PWM mit 50Hz
    p.start(2.5)
    range = max - min
    pos = min + (range / 180 * degree)
    print "pos", pos
    
    p.ChangeDutyCycle(pos)
    time.sleep(0.5)
    p.stop()
    GPIO.cleanup()
  
def main(argv):
    if len(argv) == 1:
        degree = int(argv[0])
        if degree > 180 or degree < 0:
            print "Degree must be between 0 and 180"
            return
            
        print "degree", degree
        
        rotate_servo(degree)
        
        print "Rotate to " + argv[0] + "degree"
    
    else:
        print "wrong paramter length"
        
    print argv

if __name__ == "__main__":
   main(sys.argv[1:])
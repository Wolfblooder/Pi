import time
import RPi.GPIO as GPIO

sensor = '/sys/bus/w1/devices/28-01201c974288/w1_slave'
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setwarnings(False)
def readTempSensor(sensorName) :
    
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines
def extract(input):
    split = str(input)
    return split[76:81]

def turnToTemp(temperatur):
    i = (str(temperatur[:2]) + "." + str(temperatur[3:6]))
    return float(i)

def currentTemp():
    return turnToTemp(extract(readTempSensor(sensor)))

def lampOn():
    GPIO.output(21, GPIO.HIGH)

def lampOff():
    GPIO.output(21, GPIO.LOW)

def graph(temperatur):
    i = int((temperatur-18)*8)
    return ("█" * i)

while True :
    temperatur = currentTemp()
    led = "☒"
    tempSpacing = (" " * (8 - (len(str(temperatur)))))
    
    if(temperatur >= 24):
        lampOn()
        led = "☑"
    else:
        lampOff()
        led = "☒"
    print(time.strftime('%H:%M:%S') +" - " + str(temperatur)  + str(tempSpacing) + led + graph(temperatur))
#test
import time
import RPi.GPIO as GPIO

sensor = '/sys/bus/w1/devices/28-01201c974288/w1_slave'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
#maxtemp muss >= 18 sein
maxTemp = 24
warningArea = 1
scale = 1

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

def red():
    GPIO.output(21, GPIO.HIGH)
   
def yellow():
    GPIO.output(20, GPIO.HIGH)

def green():
    GPIO.output(16, GPIO.HIGH)
   

def off():
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)


def graph(temperatur):
    i = int((temperatur-(18))*8*scale)
    i = ("█" * i)
    if(len(i)< (48*scale - (24 - maxTemp)*8*scale)):
        i = i + (" " * (47*scale -((24 - maxTemp)*8*scale)- len(i))) + "|"
    return i
off()
time.sleep(1)
while True :
    temperatur = currentTemp()
    led = ""
    tempSpacing = (" " * (8 - (len(str(temperatur)))))
    
    if(temperatur >= maxTemp):
        off()
        red()
        led = "☑ "
    elif(temperatur >= (maxTemp - warningArea)):
        off()
        yellow()
        led = "☒ "
    else:
        off()
        green()
        led = "☒ "
    print(time.strftime('%H:%M:%S') +" | " + str(temperatur)  + str(tempSpacing) + led + graph(temperatur))
    

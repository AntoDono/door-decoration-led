import time
import RPi.GPIO as GPIO


ULTRA_PIN_IN = 21
ULTRA_PIN_OUT = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#set GPIO direction (IN / OUT)
GPIO.setup(ULTRA_PIN_OUT, GPIO.OUT)
GPIO.setup(ULTRA_PIN_IN, GPIO.IN)

while True:
        # set Trigger to HIGH
        # GPIO.output(ULTRA_PIN_OUT, True)
    
        # # set Trigger after 0.01ms to LOW
        # time.sleep(0.00001)
        # GPIO.output(ULTRA_PIN_OUT, False)
    
        # StartTime = time.time()
        # StopTime = time.time()

        print(GPIO.input(ULTRA_PIN_IN))
    
        # save StartTime
        # while GPIO.input(ULTRA_PIN_IN) == 0:
        #     print(f"Input: {GPIO.input(ULTRA_PIN_IN)}")
        #     StartTime = time.time()
    
        # # save time of arrival
        # while GPIO.input(ULTRA_PIN_IN) == 1:
        #     print("Waiting for arrival")
        #     StopTime = time.time()
    
        # # time difference between start and arrival
        # TimeElapsed = StopTime - StartTime
        # # multiply with the sonic speed (34300 cm/s)
        # # and divide by 2, because there and back
        # distance = (TimeElapsed * 34300) / 2

        # print(f"Distance: {distance}")
#!/usr/bin/env python 
import time
import psutil
import threading
import subprocess
import RPi.GPIO as GPIO


# ULTRA_PIN_IN = 20
# ULTRA_PIN_OUT = 21

# GPIO.setmode(GPIO.BCM)

#set GPIO direction (IN / OUT)
# GPIO.setup(ULTRA_PIN_OUT, GPIO.OUT)
# GPIO.setup(ULTRA_PIN_IN, GPIO.IN)

IP_ADDRESS = "Fetching IP"

# LED SETTINGS
LED_ROWS = 32
LED_COLS = 64
LED_BRIGHTNESS = 65
LED_SLOWDOWN_GPIO = 4
LED_REFRESH_LIMIT = 100 #in hertz
LED_NO_HARDWARE_PULSE = True

# MUSIC SETTINGS

VOLUME = 10000 # MAX VOLUME IS 32768

# music name to path
MUSIC_REFERENCE = {
    "all_i_want": "./assets/mp3/all_i_want.mp3",
    "butter": "./assets/mp3/butter.mp3",
    "padoru": "./assets/mp3/padoru.mp3",
    "amongus_drip": "./assets/mp3/amongus_drip.mp3",
    "sus_effect": "./assets/mp3/sus_effect.mp3",
    "amongus": "./assets/mp3/amongus_drip.mp3",
    "rickroll": "./assets/mp3/rickroll.mp3",
    "last": "./assets/mp3/last_christmas.mp3",
    "ifi": "./assets/mp3/ifi.mp3",
    "whitewishes": "./assets/mp3/white.mp3",
}


# Music Cycle
# True means until song finishes
MUSIC_SHOW = [
    "padoru",
    "rickroll",
    "whitewishes",
    "amongus_drip",
    "butter",
    "all_i_want",
    "last",
    "ifi",
]

# Duration is in milliseconds
# LED Cycle
LED_SHOW = [
    {"arg": ["./scripts/image-infinite", "./assets/images/WhalenMichael.jpg"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/rickroll.gif"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/sign1.gif"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/tree2.png"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/santa1.gif"], "duration": 10000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/xmas2.jpg"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/tree1.gif"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/xmas2.jpg"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/gifts1.jpg"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/sled1.jpg"], "duration": 4000, "music": None, "type": 1},
    {"arg": ["./scripts/image-infinite", "./assets/images/santa2.gif"], "duration": 10000, "music": None, "type": 1},
    
    # {"arg": ["./scripts/scroll-text", f"{DISTANCE} -f ./fonts/clR6x12.bdf -s 5 -l -1 -y 7"], "duration": 1000, "music": None},
]

INTERRUPTION = [
    {"arg": ["./scripts/scroll-text", f"'GET OUT OF MY WAY' -f ./fonts/clR6x12.bdf -s 5 -l -1 -y 7"], "duration": 5000, "music": None},
]

led_process= None
music_process = None
interrupted = False

def process_led_command(arg):
    if (not isinstance(arg, list)):
        Exception("Process LED takes a list as argument")

    command = f"{arg[0]} {arg[1]} --led-rows {LED_ROWS} --led-cols {LED_COLS} --led-brightness {LED_BRIGHTNESS} --led-slowdown-gpio {LED_SLOWDOWN_GPIO} --led-limit-refresh {LED_REFRESH_LIMIT}"
    if (LED_NO_HARDWARE_PULSE):
        command += " --led-no-hardware-pulse"
    print(command)
    return command

def process_music_command(filepath):
    command = f"mpg123 {filepath} -f {VOLUME} --aggressive"
    return command

def process_command(thread_type, arg):

    global music_process, led_process

    thread_type = thread_type.lower()

    if (thread_type == "music"):
        music_process = subprocess.run(process_music_command(arg), shell=True)
    elif (thread_type == "led"):
        led_process = subprocess.Popen(process_led_command(arg), shell=True)

def kill_process(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def led_timer(millseconds):
    global led_process
    time.sleep(millseconds/1000)
    kill_process(led_process.pid)
    led_process = None

def cycle_music():

    global music_process

    music_index = 0

    while (True):
        try:
            process_command("music", MUSIC_REFERENCE[MUSIC_SHOW[music_index]])
            music_index+=1

            if (music_index >= len(MUSIC_SHOW)):
                music_index = 0
        except KeyboardInterrupt:
            return

def cycle_led():

    global led_process

    led_index = 0
    
    while (True):
        try:

            print(IP_ADDRESS)
            
            timer_thread = threading.Thread(target=led_timer, args=[LED_SHOW[led_index]["duration"]])
            timer_thread.start()
            process_command("led", LED_SHOW[led_index]["arg"])

            led_index+=1

            while(led_process or interrupted):
                pass

            if (led_index >= len(LED_SHOW)):
                led_index = 0
        except KeyboardInterrupt:
            return

def distance():

    while True:
        # set Trigger to HIGH
        GPIO.output(ULTRA_PIN_OUT, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(ULTRA_PIN_OUT, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(ULTRA_PIN_IN) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(ULTRA_PIN_IN) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        if (distance < 200):

            global interrupted, led_process

            if (not led_process): 
                continue

            interrupted = True

            try:
                kill_process(led_process.pid)
            except:
                pass

            led_index = 0

            while (True):
                try:
                    
                    timer_thread = threading.Thread(target=led_timer, args=[INTERRUPTION[led_index]["duration"]])
                    timer_thread.start()

                    process_command("led", INTERRUPTION[led_index]["arg"])

                    led_index+=1

                    while(led_process):
                        pass

                    if (led_index >= len(INTERRUPTION)):
                        break

                except KeyboardInterrupt:
                    return

            interrupted = False


def main():

    led_cycle_thread = threading.Thread(target=cycle_led)
    music_cycle_thread = threading.Thread(target=cycle_music)
    detection_thread = threading.Thread(target=distance)

    led_cycle_thread.start()
    music_cycle_thread.start()
    # detection_thread.start()


if __name__ == '__main__':
    main()


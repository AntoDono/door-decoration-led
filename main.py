#!/usr/bin/env python 
import os
import time
import signal
import threading
import subprocess

# LED SETTINGS
LED_ROWS = 32
LED_COLS = 64
LED_BRIGHTNESS = 65
LED_SLOWDOWN_GPIO = 2
LED_REFRESH_LIMIT = 100 #in hertz
LED_NO_HARDWARE_PULSE = True

# MUSIC SETTINGS

VOLUME = 1000 # MAX VOLUME IS 32768

# music name to path
MUSIC_REFERENCE = {
    "all_i_want": "./assets/mp3/all_i_want.mp3",
    "padoru": "./assets/mp3/padoru.mp3",
    "all_i_want_remix": "./assets/mp3/all_i_want_remix.mp3",
    "sus_effect": "./assets/mp3/sus_effect.mp3",
    "amongus": "./assets/mp3/amongus_drip.mp3",
}


# Music Cycle
# True means until song finishes
MUSIC_SHOW = [
    "padoru",
    "all_i_want",
    "all_i_want_remix"
]

# Duration is in milliseconds
# LED Cycle
LED_SHOW = [
    # {"arg": ["./scripts/image-infinite", "./assets/images/xmas1.gif"], "duration": 10000, "music": None},
    # {"arg": ["./scripts/image-infinite", "./assets/images/santa1.gif"], "duration": 10000, "music": None},
    # {"arg": ["./scripts/image-infinite", "./assets/images/sled1.gif"], "duration": 10000, "music": None},
    # {"arg": ["./scripts/image-infinite", "./assets/images/tree1.gif"], "duration": 10000, "music": None},
    {"arg": ["./scripts/scroll-text", "Happy Holidays! -f ./fonts/clR6x12.bdf -s 5 -l -1 -y 7"], "duration": 15000, "music": None},
    {"arg": ["./scripts/image-infinite", "./assets/images/xmas1.jpg"], "duration": 10000, "music": None},
    {"arg": ["./scripts/image-infinite", "./assets/images/xmas2.jpg"], "duration": 10000, "music": None},
]

INTERRUPTION = [

]

led_process= None
music_process = None

def process_led_command(arg):
    if (not isinstance(arg, list)):
        Exception("Process LED takes a list as argument")

    command = f"{arg[0]} {arg[1]} --led-rows {LED_ROWS} --led-cols {LED_COLS} --led-brightness {LED_BRIGHTNESS} --led-slowdown-gpio {LED_SLOWDOWN_GPIO} --led-limit-refresh {LED_REFRESH_LIMIT}"
    if (LED_NO_HARDWARE_PULSE):
        command += " --led-no-hardware-pulse"
    print(command)
    return command

def process_music_command(filepath):
    command = f"mpg123 {filepath} -f {VOLUME}"
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
    print("LED Process Killed")
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
            
            timer_thread = threading.Thread(target=led_timer, args=[LED_SHOW[led_index]["duration"]])
            timer_thread.start()

            process_command("led", LED_SHOW[led_index]["arg"])
            led_index+=1

            while(led_process):
                pass

            if (led_index >= len(LED_SHOW)):
                led_index = 0
        except KeyboardInterrupt:
            return

def main():

    led_cycle_thread = threading.Thread(target=cycle_led)
    music_cycle_thread = threading.Thread(target=cycle_music)

    led_cycle_thread.start()
    music_cycle_thread.start()


if __name__ == '__main__':
    main()


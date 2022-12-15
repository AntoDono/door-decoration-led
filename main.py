#!/usr/bin/env python 
import os
import signal
import asyncio
import threading
import subprocess

# LED SETTINGS
LED_ROWS = 32
LED_COLS = 64
LED_BRIGHTNESS = 75
LED_SLOWDOWN_GPIO = 2
LED_REFRESH_LIMIT = 100 #in hertz
LED_NO_HARDWARE_PULSE = True

# MUSIC SETTINGS

VOLUME = 2000 # MAX VOLUME IS 32768

led_process= None
music_process = None

def process_led_command(arg):
    if (not isinstance(arg, list)):
        Exception("Process LED takes a list as argument")

    command = f"{arg[0]} {arg[1]} --led-rows {LED_ROWS} --led-cols {LED_COLS} --led-brightness {LED_BRIGHTNESS} --led-slowdown-gpio {LED_SLOWDOWN_GPIO} --led-fresh-limit {LED_REFRESH_LIMIT}"
    if (LED_NO_HARDWARE_PULSE):
        command += " --led-no-hardware-pulse"
    return command

def process_music_command(filepath):
    command = f"mpg123 {filepath} -f {VOLUME}"
    return command

def worker(thread_type, arg):

    thread_type = thread_type.lower()

    if (thread_type == "music"):
        music_process = subprocess.run(process_music_command(arg), shell=True)
    elif (thread_type == "led"):
        led_process = subprocess.run(process_led_command(arg), shell=True)


def kill_process(pid):
    os.kill(pid, signal.SIGTERM)
    

def main():

    led_thread = threading.Thread(target=worker, args=["led", ["./scripts/image-infinite", "./assets/images/xmas1.gif"]])
    music_thread = threading.Thread(target=worker, args=["music", "./assets/mp3/Merry_Christmas_Trap.mp3"])

    led_thread.start()
    music_thread.start()


if __name__ == '__main__':
    main()


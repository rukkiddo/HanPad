#!/bin/python
# Author: rukkiddo@hankut.com

from pynput import keyboard
from pynput.mouse import Button, Controller

mouse = Controller()
def_acc = 1
acc = def_acc
min_speed = 1
max_speed = 50
pause = False

holding = {
    "'8'": False,
    "'2'": False,
    "'4'": False,
    "'6'": False,
    "Key.shift": False,
}



def on_key_release(key):
    c_key = str(key)
    global acc
    if c_key in holding:
        holding[c_key] = False
        acc = def_acc

    if c_key == "<65437>":
        mouse.release(Button.left)
    if c_key == "'0'":
        mouse.release(Button.middle)
    if c_key == "'+'":
        mouse.press(Button.right)
        mouse.release(Button.right)

def on_key_press(key):
    global pause
    c_key = str(key)
    if c_key == "Key.pause":
        enable() if pause else disable()
    if pause:
        return
    global acc, min_speed, max_speed
    if c_key in holding:
        holding[c_key] = True
        acc += 1

    speed = max_speed if holding["Key.shift"] else min_speed
    speed += acc

    if hasattr(key, 'vk') and key.vk == None:
        x = 0
        y = 0
        if holding["'2'"]:
            y = speed
        if holding["'8'"]:
            mouse.move(0, -speed)
            y = -speed
        if holding["'4'"]:
            x = -speed * 2
        if holding["'6'"]:
            x = speed * 2
        mouse.move(x,y)
    if c_key == "<65437>":
        mouse.press(Button.left)
    if c_key == "'0'":
        mouse.press(Button.middle)

def enable():
    print("enabling")
    global pause
    pause = False

def disable():
    print("disabling")
    global pause
    pause = True

with keyboard.Listener(on_release = on_key_release, on_press = on_key_press) as listener:
    listener.join()

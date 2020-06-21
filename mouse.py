#!/bin/python
# Author: rukkiddo@hankut.com

from pynput import keyboard
from pynput.mouse import Button, Controller
from pathlib import Path
import xml.etree.ElementTree as ET
import os
import atexit

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
shortcuts_folder = ROOT_DIR + "/shortcuts/xfce"
# shortcuts_bak_file = ROOT_DIR + "/shortcuts/xfce/xfce4-keyboard-shortcuts.xml"
shortcuts_xml = os.path.expanduser("~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml")

mouse = Controller()
def_acc = 1
acc = def_acc
min_speed = 1
max_speed = 50
scroll_speed = 5
scroll_fast_speed = 20 # wont work because shift 3-9 is side scroll already
pause = True

holding = {
    "'8'": False,
    "'2'": False,
    "'4'": False,
    "'6'": False,
    "'3'": False,
    "'9'": False,
    "Key.shift": False,
}

mask_list = ["KP_Left",
"KP_Right",
"KP_Up",
"KP_Down",
"KP_3",
"KP_9",
"<Shift>KP_4",
"<Shift>KP_2",
"<Shift>KP_6",
"<Shift>KP_8",
"<Shift>KP_3",
"<Shift>KP_9",
"KP_Insert",
"<Shift>KP_0",
"KP_Begin",
"<Shift>KP_5",
"<Control>KP_5",
"<Shift>KP_Add",
"KP_Add",
"<Primary>KP_5",
]




def on_key_release(key):
    c_key = str(key)
    global acc
    if pause:
        return
    if c_key in holding:
        holding[c_key] = False
        acc = def_acc

    if c_key == "<65437>":
        mouse.release(Button.left)
    if c_key == "'0'" and key.vk == None:
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
    global acc, min_speed, max_speed, scroll_fast_speed, scroll_speed
    if c_key in holding:
        holding[c_key] = True
        acc += 1

    if holding["Key.shift"]:
        speed = max_speed
        scroll_y_speed = scroll_fast_speed
    else:
        speed = min_speed
        scroll_y_speed = scroll_speed
    # speed = max_speed if holding["Key.shift"] else min_speed
    speed += acc

    if hasattr(key, 'vk') and key.vk == None:
        x = 0
        y = 0
        move = False
        scroll = False
        if holding["'2'"]:
            y = speed
            move = True
        if holding["'8'"]:
            mouse.move(0, -speed)
            move = True
            y = -speed
        if holding["'4'"]:
            move = True
            x = -speed * 2
        if holding["'6'"]:
            move = True
            x = speed * 2
        if holding["'3'"]:
            scroll = True
            scroll_y = -scroll_y_speed
        if holding["'9'"]:
            scroll = True
            scroll_y = scroll_y_speed
        if move:
            mouse.move(x,y)
        if scroll:
            mouse.scroll(0, scroll_y)
        if c_key == "'0'":
            mouse.press(Button.middle)
    if c_key == "<65437>":
        mouse.press(Button.left)

def enable():
    global pause, shortcuts_folder, shortcuts_xml, mask_list
    pause = False
    
    Path(shortcuts_folder).mkdir(parents=True, exist_ok=True)

    tree = ET.parse(shortcuts_xml)
    root = tree.getroot()
    parent = root.find("./property[@name='commands']/property[@name='custom']")
    lovesh = ROOT_DIR + "/love.sh"
    for mask in mask_list:
        prop = ET.Element("property")
        prop.attrib["name"] = mask
        prop.attrib["type"] = "string"
        prop.attrib["value"] = os.path.expanduser(lovesh)
        parent.append(prop)
    result = ET.tostring(root)
    tree.write(shortcuts_xml)
    os.system("killall xfconfd & /usr/lib/xfce4/xfconf/xfconfd & xfsettingsd --replace")

def disable():
    global pause
    pause = True
    tree = ET.parse(shortcuts_xml)
    root = tree.getroot()
    lovesh = ROOT_DIR + "/love.sh"
    parent = root.find("./property[@name='commands']/property[@name='custom']")
    for el in root.findall("./property[@name='commands']/property[@name='custom']/property[@value='"+lovesh+"']"):
        parent.remove(el)
    result = ET.tostring(root)
    tree.write(shortcuts_xml)
    os.system("killall xfconfd & /usr/lib/xfce4/xfconf/xfconfd & xfsettingsd --replace")

atexit.register(disable)
disable()

with keyboard.Listener(on_release = on_key_release, on_press = on_key_press) as listener:
    listener.join()

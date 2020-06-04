#!/bin/python
# Author: rukkiddo@hankut.com

from pynput import keyboard
from pynput.mouse import Button, Controller
from pathlib import Path
import xml.etree.ElementTree as ET
import shutil, os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
shortcuts_folder = ROOT_DIR + "/shortcuts/xfce"
shortcuts_bak_file = ROOT_DIR + "/shortcuts/xfce/xfce4-keyboard-shortcuts.xml"
shortcuts_xml = os.path.expanduser("~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml")

mouse = Controller()
def_acc = 1
acc = def_acc
min_speed = 1
max_speed = 50
pause = True

holding = {
    "'8'": False,
    "'2'": False,
    "'4'": False,
    "'6'": False,
    "Key.shift": False,
}

mask_list = ["KP_Left",
"KP_Right",
"KP_Up",
"KP_Down",
"&lt;Shift&gt;KP_4",
"&lt;Shift&gt;KP_2",
"&lt;Shift&gt;KP_6",
"&lt;Shift&gt;KP_8",
"KP_Insert",
"&lt;Shift&gt;KP_0",
"KP_Begin",
"&lt;Shift&gt;KP_5",
"&lt;Shift&gt;KP_Add",
"KP_Add",
"&lt;Primary&gt;KP_5",
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
        if c_key == "'0'":
            mouse.press(Button.middle)
    if c_key == "<65437>":
        mouse.press(Button.left)

def enable():
    print("enabling")
    global pause, shortcuts_folder, shortcuts_xml, shortcuts_bak_file, mask_list
    pause = False
    
    Path(shortcuts_folder).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(shortcuts_xml, shortcuts_bak_file)

    tree = ET.parse(shortcuts_bak_file)
    root = tree.getroot()
    print(root)
    parent = root.find("./property[@name='commands']/property[@name='custom']")
    for mask in mask_list:
        prop = ET.Element("property")
        prop.attrib["name"] = mask
        prop.attrib["type"] = "string"
        prop.attrib["value"] = os.path.expanduser(ROOT_DIR + "/love.sh")
        parent.append(prop)
    result = ET.tostring(root)
    print(result)
    tree.write(shortcuts_xml)
    os.system("killall xfconfd & /usr/lib/xfce4/xfconf/xfconfd & xfsettingsd --replace")

def disable():
    print("disabling")
    global pause
    pause = True
    shutil.copyfile(shortcuts_bak_file, shortcuts_xml)
    os.system("killall xfconfd & /usr/lib/xfce4/xfconf/xfconfd & xfsettingsd --replace")


with keyboard.Listener(on_release = on_key_release, on_press = on_key_press) as listener:
    listener.join()

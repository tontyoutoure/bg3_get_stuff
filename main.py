import numpy as np
import tkinter as tk
import cv2
import win32gui
import win32con
import win32api
from ctypes import windll, byref, wintypes, sizeof
import time
import math
import json

from stuff_mover import stuff_mover

with open("promts.json") as f:
    promts = json.load(f)

def show_text(text, duration, bg3_handle):
    root = tk.Tk()
    root.overrideredirect(True)  # Removes the window frame
    root.geometry("+0+0")  # Positions the text at x=300, y=300
# transparent background and red text
    root.wm_attributes("-transparentcolor", "white")
    label = tk.Label(root, text=text,font=("Helvetica", 48), bg='white', fg='red')
    label.pack()
    is_exit = False
    # test bg3 is activated, if so, close the window
    def close_window():
        if test_bg3_activated(bg3_handle):
            root.destroy()
        else:
            #exit the program
            exit()
    root.after(duration, close_window)

    root.mainloop()

def get_bg3_corner(bg3_handle, title_bar_height=58, border_width=2):
    # You may need to adjust these values based on your application and Windows version/DPI settings
    frame = wintypes.RECT()
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    windll.dwmapi.DwmGetWindowAttribute(
        bg3_handle,
        DWMWA_EXTENDED_FRAME_BOUNDS,
        byref(frame),
        sizeof(frame)
    )
    xy_corner = frame.left + border_width, frame.top + title_bar_height
        
        
    
    # Return the content area rectangle
    return xy_corner

def find_bg3_handle():
    """Enumerate all open windows and return their titles."""
    output_handle = []
    def callback(handle, data):
        wt = win32gui.GetWindowText(handle)
        if wt.find("Baldur's Gate 3") != -1:
            output_handle.append(handle)
    
    win32gui.EnumWindows(callback, None)
    return output_handle[0]

def test_bg3_activated(bg3_handle):
    return win32gui.GetForegroundWindow() == bg3_handle









if __name__ == "__main__":
    # screenshot = get_screen_shot()
    max_level = int(input(promts["input_max_level"]))
    loop_count = int(input(promts["input_loop_count"]))
    index_str = input(promts["input_index"])
    index_list = index_str.split(",")
    conversation_number_str = input(promts["input_conversation_number"])
    conversation_number_list = conversation_number_str.split(",")

    bg3_handle = find_bg3_handle()
    show_text(promts["bg3_front"], 5000, bg3_handle)
    x, y = get_bg3_corner(bg3_handle)

    mover = stuff_mover(x, y, max_level = max_level, loop_count = loop_count)
    # mover.add_leveller(0,4)
    mover.add_leveller(int(index_list[0])-1, int(conversation_number_list[0]))
    for i in range(1, len(index_list)):
        mover.add_purchaser(int(index_list[i])-1, int(conversation_number_list[i]))
    # mover.add_purchaser(1, 1)
    # mover.add_purchaser(3, 2)

    # time.sleep(5)
    mover.move()

    # loc = reco_image_pos(screenshot, eocgs)
    



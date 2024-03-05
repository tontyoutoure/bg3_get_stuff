from image import reco_image_pos, reco_exit_icon
import json
import pyautogui
import cv2
import numpy as np
import time
import pydirectinput
import glob

with open("promts.json") as f:
    promts = json.load(f)

class stuff_mover():
    def __init__(self, window_x_start, window_y_start, max_level = 12, loop_count = 1):
        self.window_x_start = window_x_start
        self.window_y_start = window_y_start
        self.purchasers = []
        self.max_level = max_level
        self.loop_count = loop_count
        json_f = open("position_list.json")
        self.position_list = json.load(json_f)
        json_f.close()
        strategy_y_interval = (self.position_list["strategies_end"][1] - self.position_list["strategies_start"][1])/13
        self.position_list["strategies"] = []
        for i in range(14):
            self.position_list["strategies"].append([self.position_list["strategies_start"][0], self.position_list["strategies_start"][1] + int(strategy_y_interval * i)])

        icon_file_list = glob.glob("item_icons/*.png")
        self.item_icons = []
        for icon_file in icon_file_list:
            self.item_icons.append(cv2.imread(icon_file))
            self.item_icons[-1] = cv2.cvtColor(self.item_icons[-1], cv2.COLOR_BGR2RGB)


        self.current_screen = "outside" # outside, conversation_merchant, conversation_jergal, levelup, change_class, purchase
        self.current_level = 9
        self.log_level = 0

    def print(self, text, level = 1):
        if level <= self.log_level:
            print(text) 
    def add_purchaser(self, index, conversation_number):
        self.purchasers.append({"index" : index, "conversation_number" : conversation_number})

    def add_leveller(self, index, change_class_conversation_number):
        self.leveller = {"index" : index, "conversation_number" : change_class_conversation_number}

    def get_screen_shot(self):
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        
        return screenshot[self.window_y_start:self.window_y_start+1080, self.window_x_start:self.window_x_start+1920]

    def is_screen_black(self, threshold = 20):
        screenshot = self.get_screen_shot()
        return np.mean(screenshot) < threshold
    
    def wait_for_black(self, threshold = 20):
        time.sleep(0.5)
        while self.is_screen_black(threshold):
            time.sleep(0.5)
    
    def is_health_bar_showed(self):
        screenshot = self.get_screen_shot()
        health_bar_x_range = self.position_list["health_bar_x_range"]
        health_bar_y_range = self.position_list["health_bar_y_range"]
        health_bar = screenshot[health_bar_y_range[0]:health_bar_y_range[1], health_bar_x_range[0]:health_bar_x_range[1]]
        return health_bar[:,:,0].mean() > 140 and health_bar[:,:,1].mean() < 60 and health_bar[:,:,2].mean() < 60
        
    def click(self, pos, button = 'left' ):
        self.print(f"clicking {pos}")
        pydirectinput.click(self.window_x_start + pos[0], self.window_y_start + pos[1], button = button)

    def double_click(self, pos, button = 'left'):
        self.print(f"double clicking {pos}")
        pydirectinput.doubleClick(self.window_x_start + pos[0], self.window_y_start + pos[1], button = button)

    def move_to(self, pos):
        pydirectinput.moveTo(self.window_x_start + pos[0], self.window_y_start + pos[1])

    def click_npc(self):
        click_pos = self.position_list["npc_loc"]
        self.move_to(click_pos)
        time.sleep(0.1)
        if self.is_health_bar_showed():
            self.click(click_pos)
            time.sleep(0.1)
            return
        else:
            click_pos[1]+=50
            self.move_to(click_pos)
            time.sleep(0.1)
            if self.is_health_bar_showed():
                self.click(click_pos)
                time.sleep(0.1)
                return
            else:
                click_pos[1]-=100
                self.move_to(click_pos)
                time.sleep(0.1)
                if self.is_health_bar_showed():
                    self.click(click_pos)
                    time.sleep(0.1)
                    return
                else:
                    print(promts["npc_not_found"])
                    exit()

    def right_click_alot(self, times = 10):
        for i in range(times):
            time.sleep(0.1)
            self.print("right clicking")
            pydirectinput.rightClick()
            # pydirectinput.press("space")

    def start_conversation(self, character):
        self.click(self.position_list["character_icon"][character["index"]])
        self.wait_for_black()
        self.click_npc()
        
        # talk to npc
        self.right_click_alot()

        pydirectinput.press(f"{character['conversation_number']}")
        self.right_click_alot()
        
        self.wait_for_black()

    def change_class(self):
        # start from choosing leveler
        self.start_conversation(self.leveller)

        # change class
        self.click(self.position_list["warrior_class"])
        self.click(self.position_list["class_confirm"])
        self.wait_for_black()
        self.current_level = 1

    def level_up(self):
        self.click(self.position_list["character_icon"][self.leveller["index"]])
        self.wait_for_black()
        self.click(self.position_list["level_up"])
        self.wait_for_black(10)
        self.right_click_alot(5)

        if self.current_level in [1,4,8,10]:
            pass
        
        if self.current_level == 2:
            self.click(self.position_list["strategy_pos_lv2"])
            self.click(self.position_list["strategies"][0])
            self.click(self.position_list["strategies"][1])
            self.click(self.position_list["strategies"][2])
            
        if self.current_level == 3:
            self.click(self.position_list["feature_pos_lv3"])
            self.click(self.position_list["features"][0])
            
        if self.current_level == 5:
            self.click(self.position_list["feature_pos_lv3"])
            self.click(self.position_list["features"][1])
        
        if self.current_level == 6:
            self.click(self.position_list["strategy_pos_lv6"])
            self.click(self.position_list["strategies"][3])
            self.click(self.position_list["strategies"][4])

        if self.current_level == 7:
            self.click(self.position_list["feature_pos_lv3"])
            self.click(self.position_list["features"][2])

        if self.current_level == 9:
            self.click(self.position_list["strategy_pos_lv6"])
            self.click(self.position_list["strategies"][5])
            self.click(self.position_list["strategies"][6])

        if self.current_level == 11:
            self.click(self.position_list["feature_pos_lv3"])
            self.click(self.position_list["features"][2])
            

        self.click(self.position_list["level_accept"])
        self.current_level += 1
        time.sleep(0.5)
        self.right_click_alot(15)
        if self.current_level != self.max_level:
            self.click(self.position_list["return_pos"])
        self.wait_for_black()
        time.sleep(0.5)
        return
    
    def purchase(self, purchaser):
        self.start_conversation(purchaser)
        self.click(self.position_list["rearrange_button"])
        time.sleep(0.2)
        self.click(self.position_list["weight_sort_button"])
        time.sleep(0.2)



        self.double_click(self.position_list["first_slot_position"])
        time.sleep(0.5)
        x,y = reco_exit_icon(self.get_screen_shot())
        self.move_to([x-30,y+30])
        pydirectinput.mouseDown()
        self.move_to(self.position_list["container_end"])
        pydirectinput.mouseUp()

        x_start, y_start = self.position_list["item_corner_start"]
        x_end, y_end = self.position_list["item_corner_end"]
        for item_icon in self.item_icons:
            screenshot = self.get_screen_shot()
            screenshot_area = screenshot[y_start:y_end, x_start:x_end,:]
            item_x, item_y = reco_image_pos(screenshot_area, item_icon)
            if item_x >= 0:
                self.move_to([item_x+20+x_start, item_y+20+y_start])
                pydirectinput.mouseDown()
                self.move_to(self.position_list["container_inside"])
                pydirectinput.mouseUp()
                time.sleep(0.1)

        pydirectinput.press("esc")
        pydirectinput.press("esc")
        self.right_click_alot(5)


            
        


    def move(self):
        self.change_class()
        while (self.current_level < self.max_level):
            self.level_up()
            for p in self.purchasers:
                self.purchase(p)

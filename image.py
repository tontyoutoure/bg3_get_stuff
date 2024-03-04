import cv2
import numpy as np
import pyautogui
import math
import time




def reco_image_pos(screenshot, icon_image, method = cv2.TM_CCORR_NORMED, threshold = 0.95):
    screenshotR, screenshotG, screenshotB = cv2.split(screenshot)
    icon_imageR, icon_imageG, icon_imageB = cv2.split(icon_image)
    resultR = cv2.matchTemplate(screenshotR, icon_imageR, method)
    resultG = cv2.matchTemplate(screenshotG, icon_imageG, method)
    resultB = cv2.matchTemplate(screenshotB, icon_imageB, method)
    result = (resultB + resultG + resultR)
    loc = np.where(result >= 3*threshold)
    # add a rectangle to the screenshot
    if loc[0].size >= 1:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(screenshot, pt, (pt[0] + icon_image.shape[1], pt[1] + icon_image.shape[0]), (0,0,255), 2)
        return int(loc[1][0]), int(loc[0][0])
    if loc[0].size == 0:
        return -1, -1

def reco_exit_icon(screenshot):
    icon_image = cv2.imread("exit_icon.png")
    return reco_image_pos(screenshot, icon_image)
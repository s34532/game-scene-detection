import cv2
import numpy as np
from mss import mss
import time
import mss.tools

sct = mss.mss()
monitor = sct.monitors[1]
boundingbox = {'top': monitor['top'], 'left': monitor['left'], 'width': monitor['width'], 'height': monitor['height']}
template = cv2.imread('template.jpg', 0)
threshold = 0.7

def is_scene_detected(gray_screen, template, threshold):
    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    return np.any(res >= threshold)

def sceneDetected():
    print("scene detected code running")
    global scene_detected 
    scene_detected = False
    # Wait for scene to appear
    while not scene_detected:
        sct_img = sct.grab(boundingbox)
        screen = np.array(sct_img)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        scene_detected = is_scene_detected(gray_screen, template, threshold)
        time.sleep(0.05)  # Sleep to prevent high CPU usage

    print("Scene Detected")

def sceneEnded():
    global scene_detected

    # Wait for scene to go away
    while scene_detected:
        sct_img = sct.grab(boundingbox)
        screen = np.array(sct_img)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        scene_detected = is_scene_detected(gray_screen, template, threshold)
        time.sleep(0.05)  # Sleep to prevent high CPU usage

    print("Scene No Longer Detected, walking forward...")

while (True):
    sceneDetected()
    sceneEnded()

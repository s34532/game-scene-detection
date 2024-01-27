import cv2
import numpy as np
from mss import mss
import keyboard
import time
import pyautogui
import threading
import os
from commands import enter_sigil
from battle_status_updater import update_battle_status
from shared_state import battle_status, status_lock
import mss.tools

current_status = None
scene_detected = None
template = cv2.imread('template.jpg', 0)
threshold = 0.7
sct = mss.mss()
monitor = sct.monitors[3]
boundingbox = {'top': monitor['top'], 'left': monitor['left'], 'width': monitor['width'], 'height': monitor['height']}


def check_battle_status():
    global current_status
    while True:
        with status_lock:
            current_status = battle_status['in_battle']
        print(f"Main thread checking status: {current_status}")

        time.sleep(5)



def end_program_thread():
    print("end_program_thread started\n")
    keyboard.wait('F9')
    print("F9 pressed, stopping the program...")
    os._exit(1)
            
def wait_for_hotkey(key):
    print(f"Waiting for {key} to be pressed...")
    keyboard.wait(key)
    print(f"{key} pressed, starting the program...")

def is_scene_detected(gray_screen, template, threshold):
    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    return np.any(res >= threshold)

def sceneDetected():
    global scene_detected 
    scene_detected = False
    # Wait for scene to appear
    while not scene_detected:
        sct_img = sct.grab(boundingbox)
        screen = np.array(sct_img)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        scene_detected = is_scene_detected(gray_screen, template, threshold)
        time.sleep(0.1)  # Sleep to prevent high CPU usage

    print("Scene Detected")

def sceneEnded():
    global scene_detected

    # Wait for scene to go away
    while scene_detected:
        sct_img = sct.grab(boundingbox)
        screen = np.array(sct_img)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        scene_detected = is_scene_detected(gray_screen, template, threshold)
        time.sleep(0.1)  # Sleep to prevent high CPU usage

    print("Scene No Longer Detected, walking forward...")

def main():

    global exit_thread_flag
    runs = 0
    end_thread = threading.Thread(target = end_program_thread)
    end_thread.start()


    check_status_thread = threading.Thread(target=check_battle_status)
    check_status_thread.start()

    status_thread = threading.Thread(target=update_battle_status)
    status_thread.start()

    wait_for_hotkey('F8')

    while True:
        enter_sigil()

        sceneDetected()
        sceneEnded()
            
        pyautogui.keyDown('w')
        time.sleep(3)
        pyautogui.keyUp('w')

        # Perform clicks
        time.sleep(6)
        print("press a and space")
        pyautogui.moveTo(2007, 1031)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.click()

        time.sleep(6)
            
        while current_status == False:
            time.sleep(1)

        print("w key down")
        pyautogui.keyDown('w')


        sceneDetected()
        exit_thread_flag = True
        pyautogui.keyUp('w')
        print("Thread ended")
        sceneEnded()
            
        runs = runs + 1

        if (runs > 1):
            print("The dungeon has been run: " + str(runs) + " times!")
        else:
            print("The dungeon has been run: " + str(runs) + " time!")

        time.sleep(3)



if __name__ == "__main__":
    main()
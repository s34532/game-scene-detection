import cv2
import numpy as np
from mss import mss
import keyboard
import time
import pyautogui
import threading
import random

exit_thread_flag = False

def thread_w_key():
    print("thread started...")
    while not exit_thread_flag:  # Check the flag before each iteration
        pyautogui.keyDown('w')
        random_interval = random.uniform(0, 2)
        time.sleep(random_interval)
        pyautogui.keyUp('w')

def wait_for_hotkey(key):
    print(f"Waiting for {key} to be pressed...")
    keyboard.wait(key)
    print(f"{key} pressed, starting the program...")

def is_scene_detected(gray_screen, template, threshold):
    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    return np.any(res >= threshold)

template = cv2.imread('template.jpg', 0)
threshold = 0.7

sct = mss()
monitor = sct.monitors[3]
bbox = {'top': monitor['top'], 'left': monitor['left'], 'width': monitor['width'], 'height': monitor['height']}

wait_for_hotkey('F8')

while True:
    # Check for F9 key press to exit the program
    if keyboard.is_pressed('F9'):
        print("F9 pressed, stopping the program...")
        break

    # Press 'x'
    print("press x")
    pyautogui.press('x')

    # Wait for scene to appear
    scene_detected = False
    while not scene_detected:
        sct_img = sct.grab(bbox)
        screen = np.array(sct_img)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        scene_detected = is_scene_detected(gray_screen, template, threshold)
        time.sleep(0.1)  # Sleep to prevent high CPU usage

    print("Scene Detected")

    # Wait for scene to go away
    while scene_detected:
        sct_img = sct.grab(bbox)
        screen = np.array(sct_img)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        scene_detected = is_scene_detected(gray_screen, template, threshold)
        time.sleep(0.1)  # Sleep to prevent high CPU usage

    print("Scene No Longer Detected, walking forward...")
    
    # Hold 'w' for 3 seconds
    pyautogui.keyDown('w')
    time.sleep(3)
    pyautogui.keyUp('w')

    # Perform clicks
    pyautogui.moveTo(1800, 800)
    time.sleep(5)
    pyautogui.moveTo(2007, 1031)
    time.sleep(0.1)
    pyautogui.click(button='left', clicks=2)

    # Sleep for 10 seconds
    time.sleep(10)

    # Hold 'w' until next scene change is detected
    w_thread = threading.Thread(target=thread_w_key)
    w_thread.start()


    scene_detected = False
    while not scene_detected:
        sct_img = sct.grab(bbox)
        screen = np.array(sct_img)
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        scene_detected = is_scene_detected(gray_screen, template, threshold)
        time.sleep(0.1)  # Sleep to prevent high CPU usage

    # Set the exit_thread_flag to True to stop the thread
    exit_thread_flag = True

    # Join the thread to wait for it to finish
    w_thread.join()

    pyautogui.keyUp('w')
    print("Next Scene Detected")

    # Reset the exit_thread_flag for the next iteration
    exit_thread_flag = False
    time.sleep(5)


# Program termination
print("Program stopped.")

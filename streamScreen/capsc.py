import pyautogui as pgui
import time

def streamsc(filepath = 'streamScreen/screen.jpg'):
    while True:
        try:
            ss = pgui.screenshot()
            ss.save(filepath)
            time.sleep(1)
        except Exception as e:
            print(f"Error occured with message: {e}")
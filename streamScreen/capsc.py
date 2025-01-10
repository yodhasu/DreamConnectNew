import pyautogui as pgui

def streamsc(filepath = 'streamScreen/screen.jpg'):
    while True:
        try:
            ss = pgui.screenshot()
            ss.save(filepath)
        except Exception as e:
            print(f"Error occured with message: {e}")
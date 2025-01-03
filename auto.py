import pyautogui as pg
import pytesseract
import keyboard
import threading
import time
from pynput.mouse import Listener


pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract' # change this to your Tesseract path

stop_flag = threading.Event()
def listen_for_stop():
    keyboard.wait('esc')
    stop_flag.set()

stop_listener = threading.Thread(target=listen_for_stop)
stop_listener.start()

region_x, region_y, region_height, region_width = 660, 460, 35, 120 # area of the button

mouse_clicked = threading.Event()
def on_click(x, y, button, pressed):
    if pressed:
        if region_x <= x <= region_x + region_width and region_y <= y <= region_y + region_height:
            mouse_clicked.set()

click_listener = Listener(on_click=on_click)
click_listener.start()

text = "placeholder"

while not stop_flag.is_set():

    if mouse_clicked.is_set():
        start_time = time.time()
        mode_screenshot = pg.screenshot(region=(665, 310, 80, 16))
        pg.click(725,425, duration=0.2)
        mode_image = mode_screenshot.convert("L")
        mode = pytesseract.image_to_string(mode_image)
        mode = mode.replace("\n", "")

        if mode == "10 words":
            screenshot = pg.screenshot(region=(500, 400, 440, 20))
            pg.click(725,425, duration=0.2) # click to get rid of mac alert that I can't turn off
            image = screenshot.convert("L")
            text = pytesseract.image_to_string(image)
            text = text.replace("\n", " ")
            pg.write(text)
            pg.press("enter")

            mouse_clicked.clear()
        
        elif mode == "30 words":
            for i in range(3):
                screenshot = pg.screenshot(region=(500, 400, 440, 20))
                pg.click(725,425, duration=0.2)
                image = screenshot.convert("L")
                text = pytesseract.image_to_string(image)
                text = text.replace("\n", " ")
                pg.write(text)

            pg.press("enter")
            mouse_clicked.clear()

        else:
            while True:
                if stop_flag.is_set():
                    break
                
                elapsed_time = time.time() - start_time
                if elapsed_time > int(mode.split()[0]):
                    break

                screenshot = pg.screenshot(region=(500, 400, 440, 20))
                pg.click(725,425, duration=0.2)
                image = screenshot.convert("L")
                text = pytesseract.image_to_string(image)
                text = text.replace("\n", " ")
                pg.write(text)
            
            mouse_clicked.clear()
    
    time.sleep(0.1)

import pyautogui
import pytesseract
import keyboard
from PIL import Image
import time
import io

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# while True:
#     if keyboard.is_pressed('esc'):
#         break
    
# keyboard.wait('ctrl')

# time.sleep(10)

# screenshot = pyautogui.screenshot(region=(400, 400, 630, 120))
# screenshot.save("screenshot.png")

screenshot = Image.open("screenshot.png")

img_byte_arr = io.BytesIO()
screenshot.save(img_byte_arr, format='PNG')
img_byte_arr.seek(0)

image = Image.open(img_byte_arr)

image = image.convert("RGB")

image_mode = screenshot.mode
print("Image Mode after conversion:", image_mode)

text = pytesseract.image_to_string(image)

print("Extracted Text:", text)
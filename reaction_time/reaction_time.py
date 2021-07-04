from PIL import ImageGrab
from selenium import webdriver
import time
import pyautogui as ptg
import numpy as np

driver = webdriver.Edge()
driver.maximize_window()
driver.get('https://humanbenchmark.com/tests/reactiontime')

#(75, 219, 106) green
#(43, 135, 209) blue

clicks = 0
bbox = (1759,399, 1760, 400)
while 1:
    ss = ImageGrab.grab(bbox=bbox)
    if (75,219,106) in np.array(ss):
        ptg.click(1760,400)
        clicks += 1
        time.sleep(2)
    
    if (43, 135, 209) in np.array(ss):
        ptg.click(1760,400)
        #time.sleep(2)
    
    if clicks == 5:
        break

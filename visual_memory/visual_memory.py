from selenium import webdriver
import time
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui as ptg
import imutils

driver = webdriver.Edge()
driver.maximize_window()
time.sleep(10)
driver.get('https://humanbenchmark.com/tests/memory')

button = driver.find_element_by_xpath("//*[contains(text(), 'Start')]")
button.click()

bbox = [428, 309, 1529, 858]
i=1
time.sleep(1)
while 1:
    #time.sleep(1)
    images = []
    for x in range(10):
        im = ImageGrab.grab(bbox=bbox)
        images.append(im)
        time.sleep(0.05)
    
    for image in images:
        image2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 157, 255, cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) == 0:
            continue
        time.sleep(2)
        try:
            for c in cnts:
                moment = cv2.moments(c)

                cX = int(moment["m10"] / moment["m00"])
                cY = int(moment["m01"] / moment["m00"])
                ptg.click(cX + bbox[0],cY + bbox[1])
        except:
            continue
        break
    i+=1
    time.sleep(1.5)

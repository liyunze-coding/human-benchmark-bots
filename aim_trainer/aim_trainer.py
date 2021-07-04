import cv2
import numpy as np
from PIL import ImageGrab
import time
import imutils
import pyautogui as ptg
from msedge.selenium_tools import Edge

def startup():
    driver = Edge()

    driver.get('https://humanbenchmark.com/tests/aim')
    #time.sleep(10)
    driver.maximize_window()

    return driver

def main(driver):
    bbox = (0,263,1896,871)
    ptg.click(949, 536)

    for _ in range(30):
        image = ImageGrab.grab(bbox=bbox)

        image2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        image2[np.where(image2 == (223,171,106))] = 0
        gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 157, 255, cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        moment = cv2.moments(cnts[0])

        cX = int(moment["m10"] / moment["m00"])
        cY = int(moment["m01"] / moment["m00"])

        ptg.click(cX + bbox[0],cY + bbox[1])
    time.sleep(5)
    driver.close()

if __name__ == '__main__':
    driver = startup()
    time.sleep(1)
    main(driver)

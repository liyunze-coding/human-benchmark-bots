from selenium import webdriver
import logging
from PIL import ImageGrab
import cv2
import numpy as np
import time
import imutils
import pyautogui as ptg
templates = []

for c in range(10):
    templates.append(cv2.imread(f'number_template/{c}.png',0))

logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger.setLevel(logging.WARNING)  # or any variant from ERROR, CRITICAL or NOTSET


driver = webdriver.Edge()
driver.maximize_window()
driver.get('https://humanbenchmark.com/tests/chimp')

button = driver.find_element_by_xpath("//*[contains(text(), 'Start Test')]")
button.click()

def filter_approximate(coords):
	initial_x = 0

	coords.sort(key=lambda x:x[1])

	for count, coord in enumerate(coords):
		x = coord[1]
		if count == 0:
			initial_x = x
			continue
		
		if x in range(initial_x-5,initial_x+6):
			coords[count] = []
		else:
			initial_x = x

	while [] in coords:
		coords.remove([])

	return coords

def recognize_number(locations):
    if len(locations) == 1:
        return locations[0][0]
    
    else:
        locations.sort(key=lambda x:x[1])

        num = ''

        for l in locations:
            num += str(l[0])

        return int(num)

def find_numbers(img, coordinates):
    numbers_locations = []
    for x,y in coordinates:
        locations = []
        number_image = img[y-40:y+40,x-40:x+40]
        
        for number, template in enumerate(templates):
            w,_ = template.shape[::-1]
            res = cv2.matchTemplate(number_image,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.95
            loc = np.where( res >= threshold)

            for pt in zip(*loc[::-1]):
                template_x = pt[0] + w
                locations.append([number,template_x])
        locations = filter_approximate(locations)
        number = recognize_number(locations)

        numbers_locations.append([number,x,y])
    
    numbers_locations.sort(key=lambda x:x[0])

    return numbers_locations

bbox = (400,200,1896,871)
time.sleep(1)

while 1:
	try:
		im = ImageGrab.grab(bbox=bbox)

		image = np.array(im)

		image[np.where(image==(65,147,214))] = 255

		gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		thresh = cv2.threshold(blurred, 157, 255, cv2.THRESH_BINARY)[1]

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		cnts = imutils.grab_contours(cnts)

		coordinates = []
		for c in cnts:
			# compute the center of the contour
			try:
				M = cv2.moments(c)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				
				coordinates.append([cX,cY])
			except:
				continue

		mouse_click_locations = find_numbers(gray, coordinates)

		for _, x, y in mouse_click_locations:
			ptg.click(bbox[0]+x,bbox[1]+y)

		driver.find_element_by_xpath("//*[contains(text(), 'Continue')]").click()
		time.sleep(0.2)
	except Exception as e:
		print(e)
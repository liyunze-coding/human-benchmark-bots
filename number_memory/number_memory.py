from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Edge()
driver.maximize_window()
driver.get('https://humanbenchmark.com/tests/number-memory')
time.sleep(10)

button = driver.find_element_by_xpath("//*[contains(text(), 'Start')]")
button.click()


def click_button(xpath):
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
        (By.XPATH, xpath)))
    element.click()


wait_seconds = 5
while 1:
    number = WebDriverWait(driver, 2).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "big-number"))).text  # driver.find_elements_by_class_name("big-number")

    bar = WebDriverWait(driver, wait_seconds).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@pattern='[0-9]*']")))
    bar.send_keys(number)
    driver.find_element_by_xpath("//*[contains(text(), 'Submit')]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[contains(text(), 'NEXT')]").click()
    wait_seconds += 1

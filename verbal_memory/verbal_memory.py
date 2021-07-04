from selenium import webdriver
import logging
import time

driver = webdriver.Edge()
driver.maximize_window()
driver.get('https://humanbenchmark.com/tests/verbal-memory')


button = driver.find_element_by_xpath("//*[contains(text(), 'Start')]")
button.click()

word_list = []
time.sleep(1)
while 1:
    try:
        word = driver.find_element_by_class_name('word').text
        
        if word in word_list:
            driver.find_element_by_xpath("//*[contains(text(), 'SEEN')]").click()
        else:
            driver.find_element_by_xpath("//*[contains(text(), 'NEW')]").click()
            word_list.append(word)
    except:
        break
#coding=utf-8
from selenium import webdriver
import time

driver = webdriver.Firefox()

driver.get("http://www.baidu.com")


time.sleep(10)
driver.quit()
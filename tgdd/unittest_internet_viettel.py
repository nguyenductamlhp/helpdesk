import unittest
from selenium import webdriver
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path=r"./chromedriver", options=chrome_options)


driver.get("https://www.thegioididong.com/tien-ich/thanh-toan-internet-viettel/")
driver.set_window_size(1920, 1053)
driver.find_element(By.ID, "txtUserCode").click()
driver.find_element(By.ID, "txtUserCode").send_keys("t008_gftth_oanhv0")
driver.find_element(By.CSS_SELECTOR, ".checkpay").click()
print(driver.current_url, driver.title)
total = driver.find_element(By.ID, "totalp")
print('total', total.text)

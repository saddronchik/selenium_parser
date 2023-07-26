import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

s = Service(executable_path="C:\\Users\\Andrew\\OneDrive\\Рабочий стол\\Python\\Selenium\\chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(service=s)

try:
    driver.maximize_window()
    driver.get('https://vk.com/')
    time.sleep(5)

    emai_input = driver.find_element(By.ID, "index_email")
    emai_input.clear()
    emai_input.send_keys('')
    emai_input.send_keys(Keys.ENTER)
    time.sleep(5)
  
    link_to_pass = driver.find_element(By.XPATH,'//span[text()="Войти при помощи пароля"]').click()
    time.sleep(5)

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("")
    password_input.send_keys(Keys.ENTER)
    time.sleep(5)
    


    pass
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
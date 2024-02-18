from selenium import webdriver

def create_driver_chrome():
    driver = webdriver.Chrome()
    return driver

def create_driver_firefox():
    driver = webdriver.Firefox()
    return driver
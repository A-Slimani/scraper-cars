from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint

completed_car_list = []

def create_driver():
  options = webdriver.ChromeOptions()
  options.add_argument('--no-sandbox')
  driver = webdriver.Chrome(options=options)
  return driver


def get_current_list(driver):
  driver.get('https://www.carsales.com.au/cars/toyota/crown/new-south-wales-state/?sort=LastUpdated')
  car_list = WebDriverWait(driver, randint(1, 5)).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing-item')))

  for car in car_list:
    current_car_obj = {}

    car_name = car.find_element(By.TAG_NAME, 'h3').text
    current_car_obj.update({'name': car_name})

    # detail_list = WebDriverWait(driver, randint(1, 5)).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'key-details__value')))
    detail_list = car.find_elements(By.CLASS_NAME, 'key-details__value')

    for detail in detail_list:
      current_car_obj.update({detail.get_attribute('data-type'): detail.text})     
    
    completed_car_list.append(current_car_obj)

if __name__ == '__main__':
  driver = create_driver()
  get_current_list(driver)
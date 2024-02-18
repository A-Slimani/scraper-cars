from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from datetime import date
from random import randint
from car_details import get_details
import csv
import os

completed_car_list = []

def create_driver():
  options = webdriver.ChromeOptions()
  options.add_argument('--no-sandbox')
  driver = webdriver.Chrome(options=options)
  return driver

# I think offset gives me the login error
def get_current_list_url_offset(driver):
  offset = 0
  while True:
    try:
      url = f'https://www.carsales.com.au/cars/toyota/crown/new-south-wales-state/?sort=LastUpdated&offset={offset}'
      driver.get(url)
      get_details(driver, completed_car_list)
      print(f'current offset: {offset}')
      offset += 12
    except:
      print('all pages completed')
      break

def get_current_list_button_offset(driver):
  url = f"https://www.carsales.com.au/cars/toyota/crown/new-south-wales-state/?sort=LastUpdated"
  driver.get(url)
  while True:
    try:
      get_details(driver, completed_car_list)
      next_page = WebDriverWait(driver, randint(1, 5)).until(EC.element_to_be_clickable((By.CLASS_NAME, 'page-link.next')))
      next_page.click()
    except: 
      print('all pages completed')
      break

if __name__ == '__main__':
  driver = create_driver()
  get_current_list_button_offset(driver)
  
  print(f"completed car list: {len(completed_car_list)}")

  if os.path.exists('cars.csv'):
    with open('cars.csv', 'r') as f:
      current_car_list = [row for row in csv.reader(f)]
    
    for car in completed_car_list:
      if car['ID'] in current_car_list:
        completed_car_list.remove(car)

    with open('cars.csv', 'a') as f:
      writer = csv.writer(f)
      writer.writerows(car.values() for car in completed_car_list)

  else:
    with open('cars.csv', 'w') as f:
      writer = csv.writer(f)
      writer.writerow(completed_car_list[0].keys())
      writer.writerows(car.values() for car in completed_car_list)
  
  driver.close()
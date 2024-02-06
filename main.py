from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
import csv

completed_car_list = []

def create_driver():
  options = webdriver.ChromeOptions()
  options.add_argument('--no-sandbox')
  driver = webdriver.Chrome(options=options)
  return driver


def get_current_list(driver):
  offset = 0
  while True:
    try:
      url = f'https://www.carsales.com.au/cars/toyota/crown/new-south-wales-state/?sort=LastUpdated&offset={offset}'
      driver.get(url)

      car_list = WebDriverWait(driver, randint(1, 5)).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing-item')))

      for car in car_list:
        current_car_obj = {}

        car_state = car.find_element(By.CLASS_NAME, 'seller-location')
        if car_state.text != 'NSW':
          continue

        car_price = car.find_element(By.CLASS_NAME, 'price').text
        current_car_obj.update({'price': car_price})


        car_name = car.find_element(By.TAG_NAME, 'h3')
        current_car_obj.update({'year': car_name.text.split()[0]})
        current_car_obj.update({'name': ' '.join(car_name.text.split()[1:])})

        current_car_obj.update({'state': car_state.text})

        detail_list = car.find_elements(By.CLASS_NAME, 'key-details__value')
        for detail in detail_list:
          current_car_obj.update({detail.get_attribute('data-type'): detail.text})     

        car_link = car_name.find_element(By.TAG_NAME, 'a')
        current_car_obj.update({'link': car_link.get_attribute('href')}) 

        completed_car_list.append(current_car_obj)

      print(f'current offset: {offset}')
      offset += 12
    except:
      print('all pages completed')
      break

if __name__ == '__main__':
  driver = create_driver()
  get_current_list(driver)
  
  print(f"completed car list: {len(completed_car_list)}")
  with open('cars.csv', 'w') as f:
    writer = csv.writer(f)

    # write the header orw
    writer.writerow(completed_car_list[0].keys())

    # write the data
    for car in completed_car_list:
      writer.writerow(car.values())
  
  driver.close()
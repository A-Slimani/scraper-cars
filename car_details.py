from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint
from datetime import date


def get_details(driver, completed_car_list) -> bool:
  car_list = WebDriverWait(driver, randint(1, 5)).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing-item')))

  for car in car_list:
    current_car_obj = {}

    car_state = car.find_element(By.CLASS_NAME, 'seller-location')
    if car_state.text != 'NSW':
      continue

    car_link = car.find_element(By.TAG_NAME, 'a')
    car_id = car_link.get_attribute('href').split('/')[-2]
    current_car_obj.update({'ID': car_id})

    current_car_obj.update({'Date': date.today().strftime("%d/%m/%Y")})

    car_price = car.find_element(By.CLASS_NAME, 'price').text
    current_car_obj.update({'Price': car_price})

    car_name = car.find_element(By.TAG_NAME, 'h3').text
    current_car_obj.update({'Year': car_name.split()[0]})
    current_car_obj.update({'Name': ' '.join(car_name.split()[1:])})

    current_car_obj.update({'State': car_state.text})

    detail_list = car.find_elements(By.CLASS_NAME, 'key-details__value')
    for detail in detail_list:
      current_car_obj.update({detail.get_attribute('data-type'): detail.text})     

    current_car_obj.update({'link': car_link.get_attribute('href')}) 

    completed_car_list.append(current_car_obj)
  
  return True
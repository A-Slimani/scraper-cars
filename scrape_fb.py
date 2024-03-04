import requests
from bs4 import BeautifulSoup

url = 'https://www.facebook.com/marketplace/sydney/vehicles?make=2318041991806363&model=666837530402641'

response = requests.get(url)

if response.status_code == 200:
    print('The request was successful.')
else:
    print('The request failed.')

soup = BeautifulSoup(response.text, 'html.parser')

print(soup.prettify())

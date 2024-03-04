import requests

url = 'https://www.facebook.com/marketplace/sydney/vehicles?make=2318041991806363&model=666837530402641'

response = requests.get(url)

with open('fb_page.html', 'wb') as f:
    f.write(response.content)
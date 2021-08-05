# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.


# About: NeoWs (Near Earth Object Web Service) is a RESTful web service for near earth Asteroid information.
# With NeoWs a user can: search for Asteroids based on their closest approach date to Earth, lookup a specific Asteroid
# with its NASA JPL small body id, as well as browse the overall data-set.

import requests

apikey = 'JRfxY55SSM9LaF9zcBFim8Rgtycs91dbtsq7pe5H'
user_date = input("Enter a date to search for asteroids (YYYY-MM-DD):")

url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date={user_date}&api_key={apikey}'

response = requests.get(url=url)

if not response.ok:
    print("Error")
    exit()

with open('search_results.json', 'w', encoding="utf-8") as outfile:
    outfile.write(response.content.decode("utf-8"))

print("The response is saved to search_results")

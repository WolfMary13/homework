# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json


username = input("Username GitHub: ")
url = f'https://api.github.com/users/{username}/repos'
response = requests.get(url=url)

if response.status_code == 404:
    print("User doesn't exist")
    exit()
elif not response.ok:
    print("Error")
    exit()

with open('user_repos.json', 'w', encoding="utf-8") as outfile:
    outfile.write(response.content.decode("utf-8"))

print("The response is saved to user_repos")



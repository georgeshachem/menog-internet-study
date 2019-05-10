import requests
from bs4 import BeautifulSoup
import json

with open('countries.json', 'r') as f:
    countries = json.load(f)

url = 'https://www.speedtestserver.com'
data = requests.get(url)

servers = dict()
for country, country_code in countries.items():
    servers[country_code] = list()
html = BeautifulSoup(data.text, 'html.parser')

all_servers = html.find('tbody').find_all('tr')

for server in all_servers:
    data = server.find_all('td')
    server_country = data[0].get_text()
    if server_country in list(countries.keys()):
        servers[countries[server_country]].append({'host': data[3].get_text().split(':')[0], 'id': data[4].get_text()})

with open("speedtest_servers.json", "w") as f:
    json.dump(servers, f, indent=4, sort_keys=True)

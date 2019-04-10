import requests
from bs4 import BeautifulSoup
import json

with open('countries.txt', 'r') as f:
    countries = f.readlines()
countries = list(map(lambda s: s.strip(), countries))
print(countries)

url = 'https://www.speedtestserver.com'
data = requests.get(url)

servers = dict()
for country in countries:
    servers[country] = list()
print(servers)
html = BeautifulSoup(data.text, 'html.parser')

all_servers = html.find('tbody').find_all('tr')

for server in all_servers:
    data = server.find_all('td')
    server_country = data[0].get_text()
    if server_country in countries:
        servers[server_country].append({'host': data[3].get_text(), 'id': data[4].get_text()})

with open("speedtest_servers.json", "w") as f:
    json.dump(servers, f, indent=4, sort_keys=True)

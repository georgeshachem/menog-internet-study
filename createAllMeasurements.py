import json
import os
import requests

with open('speedtest_servers.json', 'r') as f:
    servers = json.load(f)

with open('countries.txt', 'r') as f:
    countries = f.readlines()
    countries = list(map(lambda s: s.strip(), countries))

for source_country in countries:
    filename = "measurements/{}.txt".format(source_country)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+') as f:
        r = requests.get("https://restcountries.eu/rest/v2/name/{}".format(source_country))
        f.write("Measurements from: {} ({})\n".format(source_country, r.json()[0]['alpha2Code']))
        f.write("+++++++++++++++++++++++++++++++++++++++++++\n")
        f.write("\n")
        for destination_country, destination_country_servers in servers.items():
            f.write("Measurements to: {}\n".format(destination_country))
            for speedtest_server in destination_country_servers:
                f.writelines("Server: {}\n".format(speedtest_server['host']))
            f.write("\n")
            f.write("===============================================")
            f.write("\n")

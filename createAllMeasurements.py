import json
import os
import requests
from datetime import datetime
from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    AtlasSource,
    AtlasCreateRequest
)

ATLAS_API_KEY = ""

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
        source_country_code = r.json()[0]['alpha2Code']
        f.write("Measurements from: {} ({})\n".format(source_country, source_country_code))
        f.write("+++++++++++++++++++++++++++++++++++++++++++\n")
        f.write("\n")
        for destination_country, destination_country_servers in servers.items():
            f.write("Measurements to: {}\n".format(destination_country))
            for speedtest_server in destination_country_servers:
                ping = Ping(af=4, target=speedtest_server['host'],
                            description="From {} to {}".format(source_country, destination_country))
                traceroute = Traceroute(
                    af=4,
                    target=speedtest_server['host'],
                    description="From {} to {}".format(source_country, destination_country),
                    protocol="ICMP",
                )
                source = AtlasSource(type="country", value=source_country_code, requested=5)
                atlas_request = AtlasCreateRequest(
                    start_time=datetime.utcnow(),
                    key=ATLAS_API_KEY,
                    measurements=[ping, traceroute],
                    sources=[source],
                    is_oneoff=False
                )
                (is_success, response) = atlas_request.create()
                if is_success:
                    f.writelines(
                        "Server: {} - Measurement ID: {}\n".format(speedtest_server['host'], response['measurements']))
                else:
                    f.writelines(
                        "Server: {} - Failed: {}\n".format(speedtest_server['host'], response['error']['detail']))
            f.write("\n")
            f.write("===============================================")
            f.write("\n")

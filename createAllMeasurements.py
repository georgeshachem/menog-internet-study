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

ATLAS_API_KEY = "INSERT_YOUR_API_KEY"

with open('speedtest_servers.json', 'r') as f:
    servers = json.load(f)

with open('countries.txt', 'r') as f:
    countries = f.readlines()
    countries = list(map(lambda s: s.strip(), countries))

for source_country in countries:
    measurements = dict()
    r = requests.get("https://restcountries.eu/rest/v2/name/{}".format(source_country))
    source_country_code = r.json()[0]['alpha2Code']
    for destination_country, destination_country_servers in servers.items():
        measurements[destination_country] = list()
        for index, speedtest_server in enumerate(destination_country_servers):
            if index == 3:
                break
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
                measurements[destination_country].append(
                    {"host": speedtest_server['host'], "is_success": is_success,
                     "measurement_id": response['measurements']})
            else:
                measurements[destination_country].append(
                    {"host": speedtest_server['host'], "is_success": is_success})

    filename = "measurements/{}.json".format(source_country)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(measurements, f, indent=4, sort_keys=True)

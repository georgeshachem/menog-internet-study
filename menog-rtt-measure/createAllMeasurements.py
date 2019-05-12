import json
import os
from datetime import datetime, timedelta
from random import shuffle
from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    AtlasSource,
    AtlasCreateRequest
)

ATLAS_API_KEY = "INSERT_YOUR_API_KEY"

with open('working_speedtest_servers.json', 'r') as f:
    servers = json.load(f)

with open('countries.json', 'r') as f:
    countries = json.load(f)

for source_country, source_country_code in countries.items():
    measurements = dict()
    for destination_country_code, destination_country_servers in servers.items():
        measurements[destination_country_code] = list()
        shuffle(destination_country_servers)
        for index, speedtest_server in enumerate(destination_country_servers):
            if index == 3:
                break
            ping = Ping(af=4, target=speedtest_server['host'],
                        description="From {} to {}".format(source_country_code, destination_country_code),
                        interval=10800)
            traceroute = Traceroute(
                af=4,
                target=speedtest_server['host'],
                description="From {} to {}".format(source_country_code, destination_country_code),
                protocol="ICMP",
                interval=10800
            )
            source = AtlasSource(type="country", value=source_country_code, requested=5)
            atlas_request = AtlasCreateRequest(
                start_time=datetime.utcnow() + timedelta(seconds=60),
                key=ATLAS_API_KEY,
                measurements=[ping, traceroute],
                sources=[source],
                is_oneoff=False
            )
            (is_success, response) = atlas_request.create()
            if is_success:
                measurements[destination_country_code].append(
                    {"host": speedtest_server['host'], "is_success": is_success,
                     "measurement_id": response['measurements']})
            else:
                measurements[destination_country_code].append(
                    {"host": speedtest_server['host'], "is_success": is_success, "reason": response})

    filename = "measurements/{}.json".format(source_country_code)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(measurements, f, indent=4, sort_keys=True)

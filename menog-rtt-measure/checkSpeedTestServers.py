import json
from ping3 import ping

with open("all_speedtest_servers.json", "r") as f:
    all_servers = json.load(f)

working_servers = dict()

for country_code, country_servers in all_servers.items():
    working_servers[country_code] = list()
    for server in country_servers:
        try:
            if ping(server['host']) is not None:
                working_servers[country_code].append(server)
        except Exception as e:
            print(e)

with open("working_speedtest_servers.json", "w") as f:
    json.dump(working_servers, f, indent=4, sort_keys=True)

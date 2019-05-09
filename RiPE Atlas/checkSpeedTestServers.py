import json
import socket
import pyping

with open("speedtest_servers.json", "r") as f:
    all_servers = json.load(f)

working_servers = dict()

for country, country_servers in all_servers.items():
    working_servers[country] = list()
    for server in country_servers:
        try:
            result = pyping.ping('82.102.232.203').ret_code
            if result == 0:
                working_servers[country].append(server)
        except Exception as e:
            print(e)

with open("working_speedtest_servers.json", "w") as f:
    json.dump(working_servers, f, indent=4, sort_keys=True)
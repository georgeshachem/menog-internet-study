import json
import socket

with open("speedtest_servers.json", "r") as f:
    all_servers = json.load(f)

working_servers = dict()

for country, country_servers in all_servers.items():
    working_servers[country] = list()
    for server in country_servers:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((server['host'], 80))
        except Exception as e:
            print(e)
            result = 1
        if result == 0:
            working_servers[country].append(server)

with open("working_speedtest_servers.json", "w") as f:
    json.dump(working_servers, f, indent=4, sort_keys=True)
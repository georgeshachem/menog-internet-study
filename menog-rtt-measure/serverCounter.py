import json

with open("working_speedtest_servers.json", "r") as f:
    all_servers = json.load(f)

i = 0
for k, v in all_servers.items():
    i += len(v)
    print("{}: {}".format(k, len(v)))

print("#######################################")
print("Total Servers: {}".format(i))

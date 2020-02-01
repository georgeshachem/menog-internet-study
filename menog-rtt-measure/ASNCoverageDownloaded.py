import glob
import json
import os
import requests

with open('countries.json', 'r') as f:
    countries = json.load(f)

all_data = dict()

for country in countries.values():
    data = requests.get("https://stat.ripe.net/data/country-asns/data.json?resource={}".format(country)).json()
    all_data[country] = {"total_asn": data['data']['countries'][0]['stats']['registered']}

all_ips = dict()
for country in countries.values():
    all_ips[country] = dict()
    all_ips[country]['probes'] = set()
    all_ips[country]['speedtest'] = set()

for filepath in glob.iglob('measurements/data/*/*/*.json'):
    country_destination = os.path.normpath(filepath).split(os.sep)[-2]
    country_origin = os.path.normpath(filepath).split(os.sep)[-3]
    with open(filepath) as f:
        data = json.load(f)
    for measurement in data:
        all_ips[country_origin]['probes'].add(measurement['from'])
        all_ips[country_destination]['speedtest'].add(measurement['dst_addr'])

for country, ips in all_ips.items():
    total_asn_covered = dict()
    total_asn_covered['probes'] = set()
    total_asn_covered['speedtest'] = set()
    for ip in ips['probes']:
        while True:
            try:
                data = requests.get("https://stat.ripe.net/data/network-info/data.json?resource={}".format(ip)).json()
                total_asn_covered['probes'].add(data['data']['asns'][0])
            except Exception as e:
                print(ip, e)
            break
    for ip in ips['speedtest']:
        while True:
            try:
                data = requests.get("https://stat.ripe.net/data/network-info/data.json?resource={}".format(ip)).json()
                total_asn_covered['speedtest'].add(data['data']['asns'][0])
            except Exception as e:
                print(ip, e)
            break
    # all_data[country]["covered_asn"] = len(total_asn_covered)
    # all_data[country]["covered_percentage"] = (all_data[country]["covered_asn"]/all_data[country]["total_asn"])*100
    all_data[country]["covered_asn_probes_list"] = list(total_asn_covered['probes'])
    all_data[country]["covered_asn_speedtest_list"] = list(total_asn_covered['speedtest'])

with open("asn-coverage.json", "w") as f:
    json.dump(all_data, f, indent=4, sort_keys=True)

import requests
import json
import sys
import numpy as np
import glob
from ripe.atlas.sagan import PingResult
from ripe.atlas.sagan import Result

measurement_result_folder = "../menog-rtt-measure/measurements/"
global_rtt =[]

CountryDistance = [
[1, 487.21, 990, 432.91, 1680, 859.39, 1600, 140, 1594.86, 2238.6],
[487.21, 1, 695.24, 772.49, 1466.11, 1507.96, 2467.12, 1155.51, 1733.26, 8709.77],
[989.75, 695.24, 1, 556.83, 825.59, 1757.4, 875.48, 1131.37, 751.56, 1261.73],
[432.91, 772.49, 556.83, 1, 1281.04, 1234.37, 1248.85, 574.54, 1733.26, 1808.9],
[1678.55, 1466.11, 825.59, 1281.04, 1, 2515.4, 234.96, 1816.95, 137.36, 710],
[176,1494,1744,1234.37,2515.4,1,2467.12,740,2431.72,3015.91],
[1612.56, 1559, 878, 1205, 237, 2467.12, 1, 1746.14, 2975.92, 931.81],
[141.62, 1158, 1131, 574.54, 1818, 740, 1746.14, 1, 1733, 2380],
[1580, 1404, 753, 1200, 137.36, 2431.72, 218, 1733, 1, 1078],
[2238.6, 1694, 1262, 2410, 1002, 3015.91, 931.81, 2380, 776, 1]
]

for country_folder in glob.iglob(measurement_result_folder+'data/**/'):
    country_rtt =[]
    for country_file in glob.glob(country_folder + '**/'):
        rtt_min = 1e5
        for measurement_file in glob.glob(country_file + '/*.json'):
            with open(measurement_file) as file_handler:
                json_results = json.load(file_handler)
                for result in json_results:
                    raw_result = Result.get(result)
                    if(raw_result.type != "ping"):
                        continue
                    parsed_result = PingResult.get(result)
                    if(parsed_result.rtt_min == None):
                        continue
                    if(parsed_result.rtt_min < rtt_min):
                        rtt_min=parsed_result.rtt_min
        country_rtt.append(rtt_min)
    global_rtt.append(country_rtt)
print(global_rtt)
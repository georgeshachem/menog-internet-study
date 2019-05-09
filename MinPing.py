import requests
import json
import sys
import numpy as np
import glob
from ripe.atlas.sagan import PingResult

folder_array =[]
final_folder_array =[]

CountryDistance =
[
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

def getJSON(filePathAndName):
         with open(filePathAndName, 'r') as fp:
                  return json.load(fp)

for countrycountry in glob.glob('**/**/'):

         Lmin = 999999
         folder_array =[]
         for countryfile in glob.glob(countrycountry + '**/'):
                  
                  Lmin = 999999
                  for file in glob.glob(countryfile + '/*.json'):
                           print(file)
                           myObject = getJSON(file)
                           if(myObject[0].get('type') == 'ping'):

                                    res_file = file
                                    with open(res_file) as res_handler:
                                        json_results = json.load(res_handler)
                                        for result in json_results:
                                             parsed_result = PingResult.get(result)
                                             if(parsed_result.rtt_min == None):
                                                      parsed_result.rtt_min=9999
                                             if(parsed_result.rtt_min < Lmin):
                                                      Lmin=parsed_result.rtt_min
                  folder_array.append(Lmin)
         final_folder_array.append(folder_array)
print(final_folder_array)

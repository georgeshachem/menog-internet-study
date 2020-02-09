import glob
import os
import ntpath
import json
from datetime import datetime

from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    AtlasSource,
    AtlasCreateRequest
)

ATLAS_API_KEY = ""

for filepath in glob.iglob('measurements/*.json'):
    source_country_code = os.path.splitext(ntpath.basename(filepath))[0]
    with open(filepath) as f:
        data = json.load(f)
    for destination_country_code, measurements in data.items():
        for elt in measurements[:]:
            if elt['is_success'] is False:
                measurements.remove(elt)

                ping = Ping(af=4, target=elt['host'],
                            description="From {} to {}".format(source_country_code, destination_country_code),
                            interval=10800)
                traceroute = Traceroute(
                    af=4,
                    target=elt['host'],
                    description="From {} to {}".format(source_country_code, destination_country_code),
                    protocol="ICMP",
                    interval=10800
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
                    measurements[destination_country_code].append(
                        {"host": elt['host'], "is_success": is_success,
                         "measurement_id": response['measurements']})
                else:
                    measurements[destination_country_code].append(
                        {"host": elt['host'], "is_success": is_success,
                         "reason": response})

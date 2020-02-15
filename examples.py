import asyncio
import os

import aiohttp
from pygti.auth import Auth
from pygti.const import *
from pygti.gti import *

try:
    from dotenv import load_dotenv

    load_dotenv()

    GTI_USER = os.getenv("GTI_USER")
    GTI_PASS = os.getenv("GTI_PASS")
except ImportError:
    pass

if not (GTI_USER and GTI_PASS):
    print("To run the examples, enter your credentials for the GTI API.")
    GTI_USER = input("GTI Username: ")
    GTI_PASS = input("GTI Password: ")


async def main():
    async with aiohttp.ClientSession() as session:

        auth = Auth(session, GTI_USER, GTI_PASS)
        gti = GTI(auth)

        print("Example 1: init()")
        ir = await gti.init()
        print(ir)

        print()
        print("Example 2: checkName()")
        cn = await gti.checkName({"theName": {"name": "Wartenau"}})
        print(cn)

        print()
        print("Example 3: getRoute()")
        payload = {
            "version": 37,
            "language": "de",
            "start": {
                "name": "Ritterstraße",
                "city": "Hamburg",
                "combinedName": "Ritterstraße",
                "id": "Master:60904",
                "type": "STATION",
                "coordinate": {"x": 10.046196, "y": 53.567617},
            },
            "dest": {
                "name": "Wartenau",
                "city": "Hamburg",
                "combinedName": "Wartenau",
                "id": "Master:10901",
                "type": "STATION",
                "coordinate": {"x": 10.035515, "y": 53.56478},
            },
            "time": {"date": "heute", "time": "jetzt"},
            "timeIsDeparture": True,
            "realtime": "REALTIME",
        }
        gr = await gti.getRoute(payload)
        print(gr)

        print()
        print("Example 4.1: departureList()")
        dl = await gti.departureList(
            {
                "station": {
                    "name": "Wartenau",
                    "id": "Master:10901",
                    "type": "STATION",
                },
                "time": {"date": "heute", "time": "jetzt"},
                "maxList": 5,
                "maxTimeOffset": 200,
                "useRealtime": True,
            }
        )

        print(dl)

        print()
        print("Example 4.2: departureList(), return filters")
        dl = await gti.departureList(
            {
                "station": {
                    "name": "Wartenau",
                    "id": "Master:10901",
                    "type": "STATION",
                },
                "time": {"date": "heute", "time": "jetzt"},
                "maxList": 5,
                "maxTimeOffset": 200,
                "useRealtime": True,
                "returnFilters": True,
            }
        )
        print(dl)

        print()
        print("Example 5: getTariff()")
        gT = await gti.getTariff(
            {
                "scheduleElements": [
                    {
                        "departureStationId": "Master:10950",
                        "arrivalStationId": "Master:37979",
                        "lineId": "DB-EFZ:RE8_DB-EFZ_Z",
                    }
                ],
                "departure": {"date": "16.02.2020", "time": "8:04"},
                "arrival": {"date": "16.02.2020", "time": "8:29"},
            }
        )
        print(gT)

        print("Example 7: listStations()")
        # used a older dataReleaseID to show changes since then in the response
        ls = await gti.listStations({"dataReleaseID": "32.17.02"})
        print(ls)

        print()
        print("Example 8: listLines()")
        ll = await gti.listLines({"dataReleaseID": "32.17.02"})
        print(ll)

        print()
        print("Example 8: listLines()")
        ll = await gti.listLines({"dataReleaseID": "32.17.02"})
        print(ll)

        print()
        print("Example 10: getIndividualRoute()")
        payload = {
            "starts": [
                {"type": "ADDRESS", "coordinate": {"x": 9.92496, "y": 53.563494}}
            ],
            "dests": [
                {"type": "ADDRESS", "coordinate": {"x": 9.924269, "y": 53.562925}}
            ],
            "maxLength": 10000,
            "serviceType": "BICYCLE",
            "profile": "BICYCLE_NORMAL",
            "speed": "NORMAL",
        }
        indRoute = await gti.getIndividualRoute(payload)
        print(indRoute)

        print()
        print("Example 13: stationInformation()")
        si = await gti.stationInformation(
            {"station": {"name": "Wartenau", "id": "Master:10901", "type": "STATION"}}
        )
        print(si)


asyncio.run(main())

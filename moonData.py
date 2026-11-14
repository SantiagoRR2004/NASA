import requests
import math
import csv

URL = (
    "https://pds-geosciences.wustl.edu/lro/urn-nasa-pds-lro_diviner_derived1/"
    "data_derived_gcp/global_cumul_avg_cyl_{band}_002.tab"
)


def bands():
    for latMin in range(-90, 90, 10):
        latMax = latMin + 10
        minSuffix = "n" if latMin >= 0 else "s"
        maxSuffix = "n" if latMax > 0 else "s"
        yield f"{abs(latMin):02d}{minSuffix}{abs(latMax):02d}{maxSuffix}"


maximums = {}

for band in bands():
    print(f"Downloading {band}")
    response = requests.get(URL.format(band=band), stream=True, timeout=300)
    response.raise_for_status()

    for lineNumber, rawLine in enumerate(response.iter_lines(decode_unicode=True)):
        if lineNumber == 0 or not rawLine:
            continue

        values = rawLine.replace(",", " ").split()
        longitude = float(values[0])
        latitude = float(values[1])
        localTime = float(values[2])
        tbol = float(values[10])

        if tbol in (-9998, -9999):
            continue

        cell = (
            math.floor((latitude + 90) / 10),
            math.floor((longitude + 180) / 10),
        )
        if cell not in maximums or tbol > maximums[cell][0]:
            maximums[cell] = (tbol, localTime)

with open("moon_max_temperature_10deg.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "latitude_min",
            "latitude_max",
            "longitude_min",
            "longitude_max",
            "max_tbol_k",
            "max_temp_c",
            "local_time",
        ]
    )

    for latIndex in range(18):
        for lonIndex in range(36):
            maximum = maximums.get((latIndex, lonIndex))
            if maximum is None:
                continue
            tbol, localTime = maximum
            writer.writerow(
                [
                    latIndex * 10 - 90,
                    (latIndex + 1) * 10 - 90,
                    lonIndex * 10 - 180,
                    (lonIndex + 1) * 10 - 180,
                    tbol,
                    tbol - 273.15,
                    localTime,
                ]
            )

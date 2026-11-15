import requests
import tqdm
import csv
import os


def bands():
    for latMin in range(-90, 90, 10):
        latMax = latMin + 10
        minSuffix = "n" if latMin >= 0 else "s"
        maxSuffix = "n" if latMax > 0 else "s"
        yield f"{abs(latMin):02d}{minSuffix}{abs(latMax):02d}{maxSuffix}"


currentDirectory = os.path.dirname(os.path.abspath(__file__))
moonFilePath = os.path.join(currentDirectory, "moon.csv")

if not os.path.exists(moonFilePath):

    URL = (
        "https://pds-geosciences.wustl.edu/lro/urn-nasa-pds-lro_diviner_derived1/"
        "data_derived_gcp/global_cumul_avg_cyl_{band}_002.tab"
    )
    maximums = {}

    for band in tqdm.tqdm(bands(), total=18, desc="Moon Data"):
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

            point = (latitude, longitude)
            if point not in maximums or tbol > maximums[point][0]:
                maximums[point] = (tbol, localTime)

    with open("moon.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "latitude",
                "longitude",
                "max_tbol_k",
                "max_temp_c",
                "local_time",
            ]
        )

        for (latitude, longitude), (tbol, localTime) in sorted(maximums.items()):
            writer.writerow(
                [
                    latitude,
                    longitude,
                    tbol,
                    tbol - 273.15,
                    localTime,
                ]
            )

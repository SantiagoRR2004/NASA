import pandas as pd
import xarray as xr
import requests
import time
import tqdm
import io
import os

currentDirectory = os.path.dirname(os.path.abspath(__file__))
earthFilePath = os.path.join(currentDirectory, "earth.csv")

if not os.path.exists(earthFilePath):

    DATE = "2025-11-13"
    START = DATE.replace("-", "")

    url = "https://power.larc.nasa.gov/" "api/temporal/daily/regional"

    allData = []
    pbar = tqdm.tqdm(total=18 * 36, desc="Earth Data")

    for latMin in range(-90, 90, 10):

        latMax = latMin + 10

        for lonMin in range(-180, 180, 10):

            lonMax = lonMin + 10

            # print(f"Downloading lat {latMin}:{latMax}, " f"lon {lonMin}:{lonMax}")

            params = {
                "parameters": "T2M_MAX",
                "community": "RE",
                "longitude-min": lonMin,
                "longitude-max": lonMax,
                "latitude-min": latMin,
                "latitude-max": latMax,
                "start": START,
                "end": START,
                "time-standard": "UTC",
                "format": "NETCDF",
            }

            response = requests.get(url, params=params, timeout=180)

            response.raise_for_status()

            # Read NetCDF
            ds = xr.open_dataset(io.BytesIO(response.content))

            # Convert to pandas
            temp = ds["T2M_MAX"]

            tileDf = temp.to_dataframe(name="max_temp_c").reset_index()

            tileDf.columns = [c.lower() for c in tileDf.columns]

            # Standardize coordinate names
            tileDf = tileDf.rename(columns={"lat": "latitude", "lon": "longitude"})

            tileDf = tileDf[["latitude", "longitude", "max_temp_c"]]

            allData.append(tileDf)

            ds.close()

            time.sleep(0.1)
            pbar.update(1)

    pbar.close()
    df = pd.concat(allData, ignore_index=True)

    # Clean
    df["max_temp_c"] = pd.to_numeric(df["max_temp_c"], errors="coerce")

    df = df.dropna()

    df = df[df["max_temp_c"] > -900]

    df = df.drop_duplicates(subset=["latitude", "longitude"])

    # Sort
    df = df.sort_values(["latitude", "longitude"]).reset_index(drop=True)

    df.to_csv(f"earth.csv", index=False)

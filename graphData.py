from matplotlib import pyplot as plt
import pandas as pd
import earthData
import moonData

earthDF = pd.read_csv(earthData.earthFilePath)
moonDF = pd.read_csv(moonData.moonFilePath)


def graphTemperature(dataFrame, title):
    temperatureMin = dataFrame["max_temp_c"].min()
    temperatureMax = dataFrame["max_temp_c"].max()

    figure, axis = plt.subplots()
    temperaturePlot = axis.scatter(
        dataFrame["longitude"],
        dataFrame["latitude"],
        c=dataFrame["max_temp_c"],
        s=2,
        vmin=temperatureMin,
        vmax=temperatureMax,
        cmap="coolwarm",
    )

    axis.set_title(f"{title} maximum temperature")
    axis.set_ylabel("Latitude (degrees)")
    axis.set_xlabel("Longitude (degrees)")
    axis.set_xlim(-180, 180)
    axis.set_ylim(-90, 90)
    axis.grid(alpha=0.25)
    figure.colorbar(temperaturePlot, ax=axis, label="Maximum temperature (°C)")
    figure.tight_layout()

    # Save the figure to a file
    figure.savefig(f"{title}.png")


graphTemperature(earthDF, "Earth")
graphTemperature(moonDF, "Moon")

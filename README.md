# [2026 NASA Space Apps Challenge](https://www.spaceappschallenge.org/2026/) (Permanent Moon Base Locations and Mars)

This is a repository intended for the challenge [`Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars`](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/) inside the 2026 NASA Space Apps Challenge. Our idea was to train an autoencoder on Mars and Moon data and then use the reconstruction error to identify Earth locations that are similar to the Moon and Mars. This project is only an idea because we started working on the callenge the weekend of the challenge (14-15 of November 2026). We are deeply sorry that there is no good code or results.

## Data acquisition

This is something that we have never tried before, so we didn't have enought time to obtain the data. The APIs of international space agencies probably have the correct information, but extracting it is not trivial without prior experience. What we wanted to have was a matrix for the entire Earth, Moon and Mars with information about the surface of the planet like temperature, wind speed, topography, radiation, satelite image, etc. The data from Earth would probably be the average and standard deviation of the last year, while for the Moon and Mars, it would be the data we could find.

There are two files that download the maximum temperature for the Earth and Moon. But that isn't enough. The images created from this data are [Earth.png](./Earth.png) and [Moon.png](./Moon.png).

## Model training

Once all the data would have been obtained, we would have needed to select a grid size. It would have been determined by the granularity of the obtained data. A 10 km x 10 km grid would have been a good option if we had enough data and then we could use planar approximation. Let us imagine that we had a data point every kilometer, then the inputs would have been multiple matrices of size 10 x 10, one for each feature using a sliding window approach.

We would have train one autoencoder for Mars and one for the Moon. That way, the wind speed would not be included for the Moon because it does not have an atmosphere. With both trained autoencoders, we would have applied a sliding window approach to the Earth data and then we would have calculated the reconstruction error for each autoencoder. If possible, we would have ignored oceans because that would make no sense and only use more GPU resources. Finally, we would have two maps of the Earth with the reconstruction error for each autoencoder. The lower the reconstruction error, the more similar the Earth location is to the Moon or Mars.

A third autoencoder could be trained to find similar locations in the Moon to Mars, for if there is a Mars human base, it could be interesting to know if there is a similar location in the Moon. If an experiment only requires some of the features, an autoencoder could be trained with only those features.

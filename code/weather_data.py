"""Get ERA5 weather data from CDS database using feedinlib interface.

CDS: see https://cds.climate.copernicus.eu/#!/home
This script gets feedinlib input parameters from the config.mk file.
These parameters can be changed depending on the user interest.

- target_file: Netcdf file of weather data downloaded from CDS using feedinlib module
- start_date: Start date of dowloaded  weather data (default time in UTC)
- end_date: End date of downloaded weather data (default  time in UTC)
- lon: Longitude of data point (float / list)
- lat: Latitutude of data point (float / list)

see https://github.com/oemof/feedinlib/tree/dev/example for an example implementation of feedinlib.
"""
from feedinlib import era5
import xarray as xr
import sys
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/weather_data.log",
                    level=logging.DEBUG)


def get_data(start_date, end_date, lat, lon, target_file, region=1):
    """Get meteorological data from CDS using feedlib.era5 interface."""
    print("Download might take some time to finish.")

    if region == 1:
        lon = [float(x) for x in list(lon.split(","))]
        lat = [float(x) for x in list(lat.split(","))]

    else:
        lon = float(lon)
        lat = float(lat)

    print("weather data locations lon: {}, lat: {}".format(lon, lat))
    era5.\
        get_era5_data_from_datespan_and_position(variable="feedinlib",
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 latitude=lat,
                                                 longitude=lon,
                                                 target_file=target_file)

    data_meta = xr.open_dataset(target_file)
    logging.info("ERA5 weather data download done.")
    print(data_meta)
    print("Info: Weather data download completed.")


if __name__ == "__main__":
    lon = sys.argv[1]
    lat = sys.argv[2]
    target_file = sys.argv[3]
    start_date, end_date = sys.argv[4], sys.argv[5]
    region = sys.argv[6]
    get_data(start_date, end_date, lat, lon, target_file, region=int(region))

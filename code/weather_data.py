"""Get ERA5 weather data from CDS database using feedinlib interface.

CDS: see https://cds.climate.copernicus.eu/#!/home
This script gets feedinlib input parameters from the config.mk file.
These parameters can be changed depending on the user interest.

target_file  : Netcdf file of weather data downloaded from CDS using feedinlib module
start_date  : Start date of dowloaded  weather data (default time in UTC)
end_date : End date of downloaded weather data (default  time in UTC)
lon  : Longitude of data point (float / list)
lat : Latitutude of data point (float / list)

see https://github.com/oemof/feedinlib/tree/dev/example for an example implementation of feedinlib.
"""
from feedinlib import era5
import xarray as xr
import sys

weather_dir = "../data/01_raw_input_data/"


def get_data(start_date, end_date, lat, lon, target_file, region=True):
    """Get meteorological data from CDS using feedlib.era5 interface."""
    print(" This may take some time to finish downloading")
    if region is True:
        lon = [float(x) for x in list(lon.split(","))]
        lat = [float(x) for x in list(lat.split(","))]
    else:
        lon = float(lon)
        lat = float(lat)

    era5.\
        get_era5_data_from_datespan_and_position(variable="feedinlib",
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 latitude=lat,
                                                 longitude=lon,
                                                 target_file=target_file)
    data_meta = xr.open_dataset(target_file)
    print(data_meta)


if __name__ == "__main__":
    lon = sys.argv[1]
    lat = sys.argv[2]
    target_file = sys.argv[3]
    start_date, end_date = sys.argv[4], sys.argv[5]
    region = sys.argv[6]
    get_data(start_date, end_date, lat, lon, target_file, region=region)

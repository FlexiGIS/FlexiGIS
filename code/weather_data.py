"""Get ERA5 weather data from CDS database using feedinlib module format.

CDS: see https://cds.climate.copernicus.eu/#!/home
This script gets feedinlib input parameters from the config.mk file.
These parameters can be changed depending on the user interest.

target_file:=ERA5_data.nc : Netcdf file of weather data downloaded from CDS using feedinlib module
start_date:=2018-01-01 : Start date of dowloaded  weather data (default time in UTC)
end_date:= 2018-12-31 : End date of downloaded weather data (default  time in UTC)
lon:=8.15 : Longitude of data point
lat:=53.20 : Latitutude of data point

see https://github.com/oemof/feedinlib/tree/dev/example for an example implementation of feedinlib.
"""
from feedinlib import era5
import xarray as xr
import sys

weather_dir = "../data/01_raw_input_data/"


def get_data(start_date, end_date, lat, lon, target_file):
    """Get meteorological data from CDS usinf feedlib.era5 module."""
    print("This may take some time to finish downloading")
    era5.\
        get_era5_data_from_datespan_and_position(variable="feedinlib",
                                                 start_date=start_date,
                                                 end_date=end_date,
                                                 latitude=lat,
                                                 longitude=lon,
                                                 target_file=target_file)
    data_meta = xr.open_dataset(target_file)
    print(data_meta)


def feedin_solarFormat(lon, lat, target_file, to_csv=False):
    """Get weather data in pvlib format."""
    pv_data = era5.weather_df_from_era5(era5_netcdf_filename=target_file,
                                        lib="pvlib",
                                        area=[lon, lat])
    print(pv_data.head(5))

    if to_csv:

        # export to csv file
        pv_data.to_csv(weather_dir+"solar_data.csv")
    # return pv_data


def feedin_windFormat(lon, lat, target_file, to_csv=False):
    """Get weather data in windpowerlib format."""
    wind_data = era5.weather_df_from_era5(era5_netcdf_filename=target_file,
                                          lib="windpowerlib",
                                          area=[lon, lat])
    print(wind_data.head(5))

    if to_csv:
        wind_data.to_csv(weather_dir+"wind_data.csv")
    # return wind_data


if __name__ == "__main__":
    lon = float(sys.argv[1])
    lat = float(sys.argv[2])
    target_file = sys.argv[3]
    start_date, end_date = sys.argv[4], sys.argv[5]
    # get_data(start_date, end_date, lat, lon, target_file)
    feedin_solarFormat(lon, lat, target_file, to_csv=True)
    feedin_windFormat(lon, lat, target_file, to_csv=True)

"""Store Downloaded data as csv file in feedinlib format.

This script is used to write the downloaded weather data to csv file in the format
that Feedinlib understands.
"""
from feedinlib import era5
import sys

weather_dir = "../data/01_raw_input_data/"


def feedin_solarFormat(lon, lat, target_file, to_csv=False):
    """Get weather data in pvlib format."""
    pv_data = era5.weather_df_from_era5(era5_netcdf_filename=target_file,
                                        lib="pvlib",
                                        area=[lon, lat])
    print(pv_data.head(5))

    if to_csv:
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
    feedin_solarFormat(lon, lat, target_file, to_csv=True)
    feedin_windFormat(lon, lat, target_file, to_csv=True)

"""Windpower and PV power calculation from  ERA5 weather data using Feedinlib module.

This script gets input parameters from the config.mk file.
These parameters can be changed depending on the user interest.

target_file:=ERA5_data.nc : Netcdf file of weather data downloaded from CDS using feedinlib module
start_date:=2018-01-01 : Start date of dowloaded  weather data (default time in UTC)
end_date:= 2018-12-31 : End date of downloaded weather data (default  time in UTC)
lon:=8.15 : Longitude of data point
lat:=53.20 : Latitutude of data point

turbine_name:= E-101/3050 : Wind turbine type
hub_height:= 135 . Turbine hub height
wind_data:= wind_data.csv : Weather data in csv. It important (if not generated using the
"make weather_data") to load the csv file and set the columns and rows to feedinlib format.
see link below for example
https://github.com/oemof/feedinlib/blob/dev/example/simple_feedin.py

pv_panel:= Advent_Solar_Ventura_210___2008_ : Photovoltaic panel type
inverter_type:= ABB__MICRO_0_25_I_OUTD_US_208__208V_ : Inverter type
solar_data:= solar_data.csv : Weather data in csv. It important (if not generated using the
 "make weather_data") to load the csv file and set the columns and rows to feedinlib format.
see link below for example
https://github.com/oemof/feedinlib/blob/dev/example/simple_feedin.py

Note: if the weather data is dowloaded using "make weather_data", the wind and solar data csv
files generated are already set to feedinlib format, hence no further work is needed to be done
before using them for feedin calculations.

see https://github.com/oemof/feedinlib/tree/dev/example for an example implementation of feedinlib.
"""
from feedinlib import Photovoltaic, WindPowerPlant
import pandas as pd
from numpy import isnan
import sys

weather_dir = "../data/01_raw_input_data/"


def windpower_timeseries(wind_data, turbine_name, hub_height, scale=True):
    """Generate windpower feedin time-series."""
    # The available in turbine types and specification can found in the oemof database.
    # "https://github.com/wind-python/windpowerlib/blob/dev/windpowerlib/oedb/turbine_data.csv"

    turbine_spec = {
        'turbine_type': turbine_name,
        'hub_height': hub_height
    }
    wind_turbine = WindPowerPlant(**turbine_spec)
    if scale:

        feedin_wind = wind_turbine.feedin(weather=wind_data, scaling="nominal_power")
    else:

        feedin_wind = wind_turbine.feedin(weather=wind_data)

    print("Normalized windpower")
    print(feedin_wind.head(5))
    return feedin_wind


def pv_timeseries(lon, lat, solar_data, pv_panel, inverter_type, scale=True):
    """Generate PV power feedin timeseries."""
    # pv system parameters
    system_data = {
        'module_name': pv_panel,
        'inverter_name': inverter_type,
        'azimuth': 180,
        'tilt': 30,
        'albedo': 0.2
    }
    pv_system = Photovoltaic(**system_data)
    if scale:

        feedin_pv = pv_system.feedin(weather=solar_data,
                                     location=(lat, lon),
                                     scaling="peak_power")
    else:
        feedin_pv = pv_system.feedin(weather=solar_data,
                                     location=(lat, lon))
    where_nan = isnan(feedin_pv)
    feedin_pv[where_nan] = 0
    feedin_pv[feedin_pv < 0] = 0
    print("Normalized PVpower")
    print(feedin_pv.head(5))
    return feedin_pv


if __name__ == "__main__":

    lon = float(sys.argv[1])
    lat = float(sys.argv[2])
    solar_data = sys.argv[3]
    wind_data = sys.argv[4]
    turbine_name = sys.argv[5]
    pv_panel = sys.argv[6]
    inverter_type = sys.argv[7]
    hub_height = int(sys.argv[8])

    solar_data = pd.read_csv(weather_dir+"solar_data.csv", index_col=0,
                             date_parser=lambda idx: pd.to_datetime(idx, utc=True))
    # read multi-index wind data
    wind_data = pd.read_csv(weather_dir+"wind_data.csv", index_col=[0], header=[0, 1],
                            date_parser=lambda idx: pd.to_datetime(idx, utc=True))
    # convert multi-index data frame columns levels to integer
    wind_data.columns = wind_data.columns.set_levels(
        wind_data.columns.levels[1].astype(int), level=1)

    # try:
    windpower = windpower_timeseries(wind_data, turbine_name, hub_height, scale=True)
    pvpower = pv_timeseries(lon, lat, solar_data, pv_panel, inverter_type, scale=True)

    # except KeyError as err:
    #     print("key error: {0}".format(err))
    #     print("Check input parameters in cnfig.mk")

    windpower = windpower.to_frame().rename(columns={"feedin_power_plant": "wind"})
    windpower.to_csv(weather_dir+"wind_power.csv")

    pvpower = pvpower.to_frame().rename(columns={0: "pv"})
    pvpower.to_csv(weather_dir+"pv_power.csv")

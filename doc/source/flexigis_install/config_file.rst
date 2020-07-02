.. module: FlexiGIS

.. _FlexiGIS Config:

FlexiGIS Config
================
Before executing the available FlexiGIS make commands on your environment, ensure that
the config.mk file variables are properly configured. Change the following default variables
according to your respective system environment, the OpenStreetMap data location of interest 
and renewable feedin simulation parameters.

For OpenStreetMap data download (spatial location):

- URL of the OSM raw data (used for OSM raw data download)::

    # download other pbf file for other spatial areas from geofabrik
    # Change the pbf file to the pbf file name of the location of interest.

    OSM_raw_data_URL:=https://download.geofabrik.de/europe/germany/niedersachsen-latest.osm.pbf

- Name of the OSM raw data file (used for data filtering by osmosis)::
    
    # replace with downloaded pbf file name
    OSM_raw_data:=../data/01_raw_input_data/niedersachsen-latest.osm.pbf


- Name of the bounding polygon file (used for data filtering by osmosis)::

    # Use other polyfiles for other spatial areas
    polyfile:=../data/01_raw_input_data/Oldenburg.poly


For PostgreSQL database connection, parameters should be change to match user's database

- PostgreSQL connection parameters::

    # change parameter to match your database connection
    postgres_cluster:=9.1/main
    postgres_database:=database_name
    postgres_user:=user_name
    postgres_port:=port_number
    postgres_host:=host_address

To download ERA5 weather data using make weather_data, the below lines in the config.mk file should be properly edit to suit 
personal prefrence. 

- Weather data download parameters::
    
    # stores the downloade netcdf weather data as ERA5_data.nc
    target_file:= ../data/01_raw_input_data/ERA5_data.nc

    # select weather data timestamp or download period
    start_date:=2015-01-01
    end_date:= 2015-12-31

    #set region to "True" or "False" if you wish to download weather for a region or for single location
    region:=False 
    # For single coordinate or location single location (e.g single location in Oldenburg)
    lon_single_location:=8.10
    lat_single_location:=53.15

    # For download of weather data for a region (e.g: Berlin region)
    # Longitude 'west'-'East' and Latitude 'North'-'South'
    lon_region:= 13.1,13.6
    lat_region:= 52.3,52.7

- To generate renewable feedin time series::

    # defualt power system parameters
    hub_height:= 135
    # wind data in feedinlib format, for wind power simulation 
    wind_data:= wind_data.csv

    
    pv_panel:= Advent_Solar_Ventura_210___2008_
    inverter_type:= ABB__MICRO_0_25_I_OUTD_US_208__208V_
    # pv data in feedinlib format, for pv power simulation 
    solar_data:= solar_data.csv

 see `feedinlib-pv`_ on how to get available PV power system parameters and `feedinlib-wind`_ on how to get available wind power system parameters.



.. _feedinlib-wind: https://openenergy-platform.org/dataedit/view/supply/wind_turbine_library
.. _feedinlib-pv: https://github.com/oemof/feedinlib/blob/dev/example/run_pvlib_model.ipynb
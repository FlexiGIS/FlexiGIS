.. module: FlexiGIS

.. _FlexiGIS Config:

FlexiGIS Config
================
Before executing the available FlexiGIS make commands on your environment, ensure that
the config.mk file variables are properly configured. Change the following default variables
according to your respective system environment and the OpenStreetMap data location of interest.

For OpenStreetMap data download (spatial location):

- URL of the OSM raw data (used for OSM raw data download)::

    # download other pbf file for other spatial areas from geofabrik
    OSM_raw_data_URL:=https://download.geofabrik.de/europe/germany/niedersachsen-latest.osm.pbf

- Name of the OSM raw data file (used for data filtering by osmosis)::

    OSM_raw_data:=../data/01_raw_input_data/niedersachsen-latest.osm.pbf

- Name of the bounding polygon file (used for data filtering by osmosis)::

    # Use other polyfiles for other spatial areas
    polyfile:=../data/01_raw_input_data/Oldenburg.poly

For PostgreSQL database connection, parameters should be change to match user's database

- PostgreSQL connection parameters::

    postgres_cluster:=9.1/main
    postgres_database:=database_name
    postgres_user:=user_name
    postgres_port:=port_number
    postgres_host:=host_address

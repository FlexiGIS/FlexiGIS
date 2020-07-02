.. module:: FlexiGIS

.. _Directory Description:

Directory Description
======================
* code

    The folder `code` contains a "makefile" for running the FlexiGIS model, the configuration file "config.mk" which contains different parameters
    necessary to run the FlexiGIS model. Also inside the code folder are different python scripts that are executed after make commands are ran on a Linux terminal.

* data

    The folder `data` contains or should contain all the input data needed and output data generated after running FlexiGIS. The data folder contains 4 sub
    folders, which are introduced as follows:

    `01_raw_input_data`: contains the poly file of the respective investigated urban area (e.g. Oldenburg.poly). The poly file is used to filter the
    OSM planet datasets to include the data of case study. This is achieved by Osmosis and executed by running "make filter_data". However, the OSM
    planet data file is stored in this folder. The OSM planet data is filtered spatially to include urban infrastructure such as building, highway and landuse data.

        .. note::

            A sample OSM planet data file (used for in the case study) is not included
            in the present distribution of FlexiGIS because of its file size. However,
            OSM data for desired location can be downloaded via https://download.geofabrik.de
            as a pbf file.

    Other input data in this folder are, Urban style data "urban.style", Standard Load profile, economic data for storage and feedin investment optimization, and 
    weather data (wind and pv data), used for the urban energy requirements simulation.

    `02_urban_output_data`: contains the resulting abstracted urban infrastructure based on landuse, building and highway tags from the OSM planet data.

    `03_urban_energy_requirements`: contains the results data from Module II and III, which are calculated load and normalized PV and wind power time 
    series for different urban infrastructure and dispatch optimization result stored as an pickle file.

    `04_visualization`: contains plots of the abstracted urban infrastructure and aggregated load and PV energy requirements.

* doc

    Here FlexiGIS documentation and user guide are stored.

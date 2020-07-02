.. module:: FlexiGIS

.. _FlexiGIS Installation:

FlexiGIS Installation
======================
After ensuring all system requirements are satisfied, create a Python virtual environment where
the required python dependencies can be installed using pip. Python virtual environment can be
created by following the steps described `here`_.
After creating a python virtual environment, FlexiGIS can easily be installed by following these steps:

1. First clone the FlexiGIS code from the GitHub repository. In the next step, create a Python virtual 
   environment (e.g. _env_name) where the required python dependencies can be installed using pip ::   

    user@terminal:~$ git clone https://github.com/FlexiGIS/FlexiGIS.git
    user@terminal:~$ python3 -m venv _env_name    

2. activate the virtual environment ::

    user@terminal:~$ source _env_name/bin/activate

3. cd into the cloned FlexiGIS folder and install the required python dependencies ::

    (_env_name) user@terminal:~$ cd ../FlexiGIS
    (_env_name) user@terminal:~/FlexiGIS$ pip install -r requirements.txt

clone the `oemof-feedinlib`_ package from flexigis github repository(recommended) and install localy for the renewable feedin simulations. Also install the 
`oemof-solph`_ python package for the modelling and optimization of energy systems. *Note: The default solver used in by FlexiGIS is the 'CBC' slover for the linear optimization*

Running FlexiGIS
=================
To run the first two components of the FlexiGIS package, Go into the folder code,
check the parameters in `config.mk` file. Ensure you have all parameters in the config.mk properly set, see
:ref:`FlexiGIS Config`. Also ensure the poly file of the spatial location of choice is available in the data/01_raw_input_data directory before running FlexiGIS.

FlexiGIS is executed using the make command, To run the available makefile options, 
go into the code folder of the flexigis directory in your Linux terminal. The available make options are:

- make-all executes multiple make options, from download to the simulation of load and PV profiles for the urban infrastructures, and finally 
  the optimization of electricity supply and the alocated storage system::

    (_env_name) user@terminal:~/FlexiGIS/code$ make all

- make download, downloads spatial OSM data of a given location::

    (_env_name) user@terminal:~/FlexiGIS/code$ make download


- filters the downloaded OSM planet data::

    (_env_name) user@terminal:~/FlexiGIS/code$ make filter_data


- exports the spatially filtered OSM data to a PostgreSQL database using osm2pgsql::

    (_env_name) user@terminal:~/FlexiGIS/code$ make export_data

- extract highway, building and landuse data from filtered OSM data, stores them as
  shape files and also generate geopandas plots of the urban infrastructures::

    (_env_name) user@terminal:~/FlexiGIS/code$ make abstract_data


- simulates wind and pv power for given weather data::

    (_env_name) user@terminal:~/FlexiGIS/code$ make feedin


- executes the simulation of load and PV profiles for urban infrastructure::

    (_env_name) user@terminal:~/FlexiGIS/code$ make demand_supply_simulation


- provides option to either drop the database or not::

    (_env_name) user@terminal:~/FlexiGIS/code$ make drop_database


- Optimizes the feedin of the energy system and allocates the required decentralised storage in urban settings::

    (_env_name) user@terminal:~/FlexiGIS/code$ make optimization


- Download ECMWF ERA5 weather data from Climate Data Store `CDS`_, based on the coupled feedinlib interface::

    (_env_name) user@terminal:~/FlexiGIS/code$ make weather_data


- provides option to either drop the database or not::

    (_env_name) user@terminal:~/FlexiGIS/code$ make feedin_data_format

- make example can be run to generate an example simulation of aggregated load and PV profile for Oldenburg and also model 
  the optimal allocated storage and onsite renewable supply::

    (_env_name) user@terminal:~/FlexiGIS/code$ make example

The make example the routine imports spatially filtered OSM Highway, 
landuse and building data stored as csv files in the **../data/01_raw_input_data/example_OSM_data** folder. After running the FlexiGIS package 
using the makefile commands, the resulting aggregated load and PV profiles of the urban infrastructure, and optimization results are stored in 
folder **../data/03_urban_energy_requirements**, also static plots of the urban infrastructures and simulated load and PV profiles are created 
and stored in the data/04-visualisation folder. To visualise the extracted georeferenced urban infrastructures data interactively, the generated 
shape file of the extracted urban infrastructures, can be used in `QGIS`_ to generate interactive plots.

.. note::

    After running the FlexiGIS package using the makefile, the resulting aggregated
    load and PV profiles of the urban infrastructure are stored as .csv file, and the result from the 
    optimization is stored as pickle file  in folder data/03_urban_energy_requirements.

.. _here: https://packaging.python.org/tutorials/installing-packages
.. _QGIS: https://www.qgis.org/en/site/
.. _oemof-feedinlib: https://feedinlib.readthedocs.io/en/latest/
.. _oemof-solph: https://oemof-solph.readthedocs.io/en/latest/index.html
.. _CDS: https://cds.climate.copernicus.eu/#!/home

.. toctree::
  :maxdepth: 2

  config_file

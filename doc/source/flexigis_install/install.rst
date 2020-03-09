.. module:: FlexiGIS

.. _FlexiGIS Installation:

FlexiGIS Installation
======================
After ensuring all system requirements are satisfied, create a Python virtual environment where
the required python dependencies can be installed using pip. Python virtual environment can be
created by following the steps described `here`_.
After creating a python virtual environment, FlexiGIS can easily be installed by following these steps:

1. First clone the FlexiGIS code from the GitHub repository by running::

    user@terminal:~$ git clone https://github.com/FlexiGIS/FlexiGIS.git

2. In the next step, create a Python virtual environment (e.g. _env_name) where the required python dependencies can be installed using pip::

    user@terminal:~$ python3 -m venv _env_name

3. activate the virtual environment ::

    user@terminal:~$ source _env_name/bin/activate

4. cd into the cloned FlexiGIS folder ::

    (_env_name) user@terminal:~$ cd ../FlexiGIS

5. install the required python dependencies ::

    (_env_name) user@terminal:~/FlexiGIS$ pip install -r requirements.txt

Running FlexiGIS
=================
To run the first two components of the FlexiGIS platform (Module I and II), Go into the folder code,
check the parameters in `config.mk` file. Ensure you have all parameters in the config.mk properly set, see
:ref:`FlexiGIS Config`. Also ensure the poly file of the spatial location of choice is available in the data/01_raw_input_data directory before running FlexiGIS.

FlexiGIS is executed using the make command, To run the available makefile options, go into the code directory in your Linux terminal. The available make options are:

- a::

    (_env_name) user@terminal:~/FlexiGIS/code$ make all

It executes all necessary make commands for FlexiGIS, from download to the simulation
of load and PV profiles for the urban infrastructures.

- b::

    (_env_name) user@terminal:~/FlexiGIS/code$ make download

make download, downloads spatial OSM data of a given location

- c::

    (_env_name) user@terminal:~/FlexiGIS/code$ make filter_data

filters the downloaded OSM planet data

- d::

    (_env_name) user@terminal:~/FlexiGIS/code$ make export_data

exports the spatially filtered OSM data to a PostgreSQL database using osm2pgsql

- e::

    (_env_name) user@terminal:~/FlexiGIS/code$ make abstract_data

extract highway, building and landuse data from filtered OSM data, stores them as
shape files and also generate geopandas plots of the urban infrastructures

- f::

    (_env_name) user@terminal:~/FlexiGIS/code$ make demand_supply_simulation

executes the simulation of load and PV profiles for urban infrastructure

- g::

    (_env_name) user@terminal:~/FlexiGIS/code$ make drop_database

provides option to either drop the database or not

- h::

    (_env_name) user@terminal:~/FlexiGIS/code$ make example

make example can be run to generate an example simulation of aggregated load and
PV profile for Oldenburg. After running make example, the routine imports spatially
filtered OSM Highway, landuse and building data stored as csv files in the
**../data/01_raw_input_data/example_OSM_data** folder. In other words, it runs steps *e* and *g*
using the provided example data. After running the FlexiGIS model using the makefile, the resulting
aggregated load and PV profiles, urban infrastructure data are stored as .csv data in folder **../data/03_urban_energy_requirements**,
also static plots of the urban infrastructures and simulated load and PV profiles are created and stored in the data/04-visualisation folder.
To visualise the extracted georeferenced urban infrastructures data interactively, the generated shape file of the extracted urban infrastructures,
can be used in `QGIS`_ to generate interactive plots.

.. note::

    After running the FlexiGIS model using the makefile, the resulting aggregated
    load and PV profiles, urban infrastructure data are stored as .csv data in folder
    data/03_urban_energy_requirements.

.. _here: https://packaging.python.org/tutorials/installing-packages
.. _QGIS: https://www.qgis.org/en/site/

.. toctree::
  :maxdepth: 2

  config_file

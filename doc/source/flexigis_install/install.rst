.. module:: FlexiGIS

.. _FlexiGIS Installation:

FlexiGIS Installation
======================
After ensuring all system requirements are satisfied, create a Python virtual environment where
the required python dependencies can be installed using pip. Python virtual environment can be
created by following the steps described `here`_.
After creating a python virtual environment, FlexiGIS can easily be installed by following these steps:

1. activate the virtual environment ::

    $ source virtual_env_name/bin/activate

2. clone the FlexiGIS code from the GitHub repository ::

    $ git clone https://github.com/FlexiGIS/FlexiGIS.git

3. cd into the cloned FlexiGIS folder ::

    $ cd ../FlexiGIS

4. install the required python modules in the FlexiGIS/requirement.txt file ::

    $ pip install -r requirements.txt

Running FlexiGIS
=================
To run the first two components of the FlexiGIS platform (Module I and II), Go into the folder code,
check the parameters in `config.mk` file. Ensure you have all paremeters in the config.mk properly set, see
:ref:`FlexiGIS Config`.

FlexiGIS is executed using the make command, the available options are:

- a::

    $ make all

It executes all necessary make commands for FlexiGIS, from download to the simulation
of load and PV profiles for the urban infrastructures.

- b::

    $ make download

make download, downloads spatial OSM data of a given location

- c::

    $ make filter_data

filters the downloaded OSM planet data

- d::

    $ make export_data

exports the spatially filtered OSM data to a PostgreSQL database

- e::

    $ make abstract_data

extract highway, building and landuse data from filtered OSM data

- f::

    $ make demand_supply_simulation

executes the simulation of load and PV profiles for urban infrastructure

- g::

    $ make drop_database

provides option to either drop the database or not

- h::

    $ make example

make example can be run to generate an example simulation of aggregated load and
PV profile for Oldenburg. After running make example, the routine imports spatially
filtered OSM Highway,landuse and building data stored as csv files in the
**../data/01_raw_input_data/example_OSM_data** folder. In other words, it runs steps *e* and *g*
using the provided example data.

.. note::

    After running the FlexiGIS model using the makefile, the resulting aggregated
    load and PV profiles, urban infrastructure data are stored as .csv data in folder
    data/03_urban_energy_requirements.

.. _here: https://packaging.python.org/tutorials/installing-packages

.. toctree::
  :maxdepth: 2

  config_file

# FlexiGIS: an open source GIS-based platform for modelling energy systems and flexibility options in urban areas.

Author: Alaa Alhamwi alaa.alhamwi@dlr.de

Organisation: German Aerospace Center (DLR) Institute of Networked Energy Systems https://www.dlr.de/ve/

Date: 13.12.2019

Copyright: FlexiGIS code is licensed under the 3-Clause BSD License https://opensource.org/licenses/BSD-3-Clause

FlexiGIS stands for flexibilisation in Geographic Information Systems (GIS). It extracts, filters and clusters the geo-referenced urban energy infrastructure, simulates the local electricity consumption and power generation from on-site renewable energy resources, and allocates the required decentralised storage in urban settings. FlexiGIS investigates systematically different scenarios of self-consumption, it analyses the characteristics and roles of flexibilisation technologies in promoting higher autarky levels in cities. The extracted urban energy infrustructure are based mainly on OpenStreetMap data. 

The OpenStreetMap data is available under the Open Database License (ODbL). A description of the ODbL license is available at the webpage http://opendatacommons.org/licenses/odbl.
OpenStreetMap cartography is licensed as CC BY-SA. For more information on the copyright of OpenStreetMap please visit the link http://www.openstreetmap.org/copyright. The OpenStreetMap data distributed is available under the Open Database License ODbL. For more information, please visit the OpenStreetMap web page openstreetmap.org.
The datasets can be redistributed and/or modified resulted by FlexiGIS under the same licenses and copyright.

The FlexiGIS code is licensed under the BSD-3-Clause, "New BSD License" or "Modified BSD License". Redistribution and use in source and binary forms, with or without modification, are permitted. For more information concerning the BSD-3C and the description of the terms under which you can use the FlexiGIS code, please visit https://opensource.org/licenses/BSD-3-Clause.

## System requirements
FlexiGIS is developed and tested on Linux (Ubuntu 16.04.6). The tools and software used in FlexiGIS and their versions are listed in the following:

* Operating system: Ubuntu 16.04.6 LTS, Release: 16.04, Codename: xenial
* PostgreSQL version: 11.2 (64-bit)
* PostGIS version: 1.5.3
* osmosis version: 0.44.1
* osm2pgsql version: 0.88.1 (64bit id space)
* GNU Make version: 4.2.1
* Python: 3.6.7
* GNU bash: 4.3.48(1)-release (x86_64-pc-linux-gnu)


PostgreSQL: To install PostgreSQL, refer to the webpage: http://www.postgresql.org/. Please note that you need at least the version or higher to run FlexiGIS.

Osmosis: To use Osmosis, unzip the distribution (which can be obtain from the webpage: http://wiki.openstreetmap.org/wiki/Osmosis) in the location of your choice. On unix/linux systems, make the bin/osmosis script executable (ie. chmod u+x osmosis). If desired, create a symbolic link to the osmosis script somewhere on your path (eg. ln -s appdir/bin/osmosis ~/bin/osmosis).

osm2pgsql: Instruction are available on how to download and install osm2pgsql for Linux systems on the webpage: http://wiki.openstreetmap.org/wiki/Osm2pgsql.

Python: Ensure you can run python (with version 3 and above) on your OS. Python can be downloaded following this link https://www.python.org/downloads/ or Anaconda distro from https://www.anaconda.com/distribution/ .

## Getting Started
To use the FlexiGIS model download the FlexiGIS code and data folder as a zip file or clone the
 repository from the FlexiGIS GitHub repo. After downloading the FlexiGIS code, unzip the folder FlexiGIS in the location of your choice. The file structure of the FlexiGIS code folder is as follows:

* FlexiGIS
    * ├── code
    * ├── data
    * │   ├── 01_raw_input_data
    * │   ├── 02_urban_output_data
    * │   │   └── temp
    * │   ├── 03_urban_energy_requirements
    * │   └── 04_Visualisation
    * ├── doc
    * │   ├── AUTHOR
    * │   ├── BSD License.pdf
    * │   ├── COPYING
    * │   ├── LICENSE
    * │   ├── README.md
    * └── requirements.txt

  
## Installation
After making sure all system requirements are satisfied, create a Python virtual environment where the required python dependencies can be installed using pip. Python virtual
environment can be created by following the steps from https://packaging.python.org/tutorials/installing-packages/ . After creating a python virtual environment, install
the required python dependencies by running:

activate the virtual environment: `source virtual_env_name/bin/activate`

cd into the unzipped or cloned FlexiGIS directory: `cd ../FlexiGIS`

install requirements: `pip install -r requirements.txt`

##### FlexiGIS directory description

`code:` The folder code contains a "makefile" for running the FlexiGIS model and the configuration file "config.mk". The "config.mk" file contains different parameters necessary
 to run the FlexiGIS model.

`data:` The folder data contains all the data needed and generated by the FlexiGIS code. The FlexiGIS code is provided with the input and output data of the FlexiGIS model. The folder data contains 4 sub folders, which are introduced as follows:

The folder 01_raw_input_data contains the poly file of the respective invistegated urban area (e.g. Oldenburg.poly). The poly file is used to filter the OSM planet datasets to include the data of case study. This is achieved by Osmosis and executed by "make filter_data". The OSM planet data is filtered spatially to include urban infrastructure like `building`, `highway` and `landuse`. This folder should contain the OSM planet data file. It is not included in the present distribution of FlexiGIS because of its size. It can be downloaded from: http://ftp5.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org/planet.* The the resulting filtered OSM power data is stored in folder 01_raw_input_data. An example is provided with the FlexiGIS code as file niedersachsen-latest.osm.pbf.

Urban style data "urban.style", Weather data "weather-data.csv", Standard load profile data "SLP.csv" which are all input data are also saved in the 01_raw_input_data directory.

The resulting abstracted urban infrastructure based on landuse category: agriculture, education, commercial, residential,industrial and highway, are generated and saved as .csv data files in the
 02_urban_output_data directory. The temp directory is created inside 02_urban_output_data when the code is run to store temporary generated files, which are used by the code. The contents in the temp directory are deleted automatically after the abstraction is complete.

In 03_urban_energy_requirements directory, aggregated load and PV data for the urban infrastructure are saved as output csv. Also the load time series for different urban infrastructure (according to landuse) are  saved as output csv files.
Plots of the abstracted urban infrastructure and aggregated load and PV requirements are saved in folder 04_visualization.

`doc:` A primary user guide of the FlexiGIS code and model  is provided in the folder doc.

## Running FlexiGIS

To run FlexiGIS execute the following steps:

1. Download the FlexiGIS folder and unzip it in the location of your choice.

2. Go to the folder code, check the parameters in config.mk file.

The available makefile options are:

a. `make all`

b. `make download`

c. `make filter_data`

d. `make export_data`

e. `make abstract_data`

f. `make demand_supply_simulation`

g. `make drop_database`

3. After running the FlexiGIS model using the makefile, the resulting aggregated load and PV profiles, urban infrastructure data are stored as .csv data in folder data/03_urban_energy_requirements.
https://github.com/FlexiGIS/FlexiGIS.git
## Documentation

A detailed documentation of the FlexiGIS code  is available in the user guide (in folder doc).
The user guide includes detailed information about the FlexiGIS code structure, how to run the FlexiGIS model. Moreover, the user guide includes information about the simplifications and assumptions of the FlexiGIS model as well as information about how the OSM data are used.

## Help

*In case of any questions, comments or suggestions please do not hesitate to contact us by email via developers(at)FlexiGIS.de.*

*If you would like to be informed about developments from within the project and the availability of new software and releases please register for our newsletter by sending an email to:
flexigis-subscribe(at)dlr.de.*

## Contributors
Project team:

Dr. Wided Medjroubi (project leader)

Dr. Alaa Alhamwi (FlexiGIS main author)

MSc. Chinonso C. Unaichi

## Contact

*Contact email: flexigis-developers(at)dlr.de.*




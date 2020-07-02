.. module:: FlexiGIS

.. _Getting started:

Getting Started
===============
FlexiGIS is developed and tested on Linux (Ubuntu 16.04.6). The tools and software
used and their versions are listed in the following:

* Operating system: Ubuntu 16.04.6 LTS, Release: 16.04, Codename: xenial
* PostgreSQL version: 11.2 (64-bit)
* PostGIS version: 1.5.3
* osmosis version: 0.44.1
* osm2pgsql version: 0.88.1 (64bit id space)
* GNU Make version: 4.2.1
* Python: 3.6.7
* GNU bash: 4.3.48(1)-release (x86_64-pc-linux-gnu)

Before running FlexiGIS ensure the following dependencies are installed.
PostgreSQL: To install `PostgreSQL`, refer to the `PostgreSQL`_ page.
Please note that you need at least the same version or higher to run FlexiGIS.

Osmosis: To use Osmosis, unzip the distribution (which can be obtain from `Osmosis`_)
in the location of your choice. On unix/linux systems, make the bin/osmosis script executable (ie. chmod u+x osmosis).
If desired, create a symbolic link to the osmosis script somewhere on your path (eg. ln -s appdir/bin/osmosis ~/bin/osmosis).

osm2pgsql: Instruction on how to download and install osm2pgsql for Linux systems
are available on `Osm2pgsql page`_.

Python: Ensure you can run python (with version 3 and above) on your OS. Download `Python`_ or the `Anaconda`_ distro.
cbc solver: See `here`_ for cbc installation instruction.

.. _PostgreSQL : http://www.postgresql.org
.. _Python : https://www.python.org/downloads
.. _Anaconda : https://www.anaconda.com/distribution
.. _Osmosis: http://wiki.OpenStreetMap.org/wiki/Osmosis
.. _Osm2pgsql page: http://wiki.openstreetmap.org/wiki/Osm2pgsql
.. _here: https://github.com/coin-or/Cbc

To use the FlexiGIS spatial-temporal package download the FlexiGIS
code and data folder as a zip file or clone the repository from the FlexiGIS GitHub repository. After
downloading the FlexiGIS code, unzip the folder FlexiGIS in the location of your choice. The file
structure of the FlexiGIS folder is as follows:

* FlexiGIS
    * ├── code
    * ├── data
    * │   ├── 01_raw_input_data
    * │   ├── *02_urban_output_data*
    * │   ├── *03_urban_energy_requirements*
    * │   └── 04_Visualisation
    * ├── doc
    * ├── README.md
    * └── requirements.txt

see :ref:`Directory Description` for detailed description of the FlexiGIS subdirectory contents.

.. note::

    folder *02_urban_output_data* and *03_urban_energy_requirements* are created as output from
    FlexiGIS code, these folders are used to store output files.

.. toctree::
   :maxdepth: 2

   flexigis_install/install
   flexigis_install/folder_description

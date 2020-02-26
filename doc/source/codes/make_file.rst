.. module:: FlexiGIS

.. _Makefile:

Makefile
=========
**Contains make rules for the automation of all flexiGIS modules.**

- Download::

    wget -nv -O $(OSM_raw_data) $(OSM_raw_data_URL)

Download  the OSM raw data from https://download.geofabrik.de

- filter_data::

    osmosis \
	--read-pbf file=$(OSM_raw_data) \
	--tag-filter accept-ways building=* --used-node \
	--bounding-polygon file=$(polyfile) \
	--buffer outPipe.0=building \
	--read-pbf file=$(OSM_raw_data) \
	--tag-filter accept-ways highway=* --used-node \
	--bounding-polygon file=$(polyfile) \
	--buffer outPipe.0=highway \
	--read-pbf file=$(OSM_raw_data) \
	--tag-filter accept-ways landuse=* --used-node \
	--bounding-polygon file=$(polyfile) \
	--buffer outPipe.0=landuse_1 \
	--read-pbf file=$(OSM_raw_data) \
	--tag-filter accept-relations landuse=* --used-node \
	--bounding-polygon file=$(polyfile) \
	--buffer outPipe.0=landuse_2 \
	--merge inPipe.0=landuse_1 inPipe.1=landuse_2 \
	--buffer outPipe.0=landuse_all \
	--merge inPipe.0=landuse_all inPipe.1=building \
	--buffer outPipe.0=landuse_building \
	--merge inPipe.0=landuse_building inPipe.1=highway \
	--write-pbf file=$(OSM_merged_data)

Merge and Filter the OSM raw geo-urban datasets using Osmosis

- export_data::

    export PGPASSWORD=$(postgres_password); createdb -U $(postgres_user) -h $(postgres_host) $(postgres_database);
    export PGPASSWORD=$(postgres_password); $(osm2pgsql_bin) -r pbf --username=$(postgres_user) --database=$(postgres_database) --host=$(postgres_host) --port=$(postgres_port) -s \
    -C $(osm2pgsql_cache) --hstore --number-processes $(osm2pgsql_num_processes) $(OSM_merged_data);

Export the Filtered OSM data to Postgres Server using osm2pgsql

- abstract_data::

    python flexigis_road.py -U $(postgres_user) -P $(postgres_port) -H $(postgres_host) -D $(postgres_database)
    python flexigis_buildings.py -U $(postgres_user) -P $(postgres_port) -H $(postgres_host) -D $(postgres_database)
    python plot_polygons.py

Execute abstraction module on filtered OSM dataset

- demand_supply_simulation::

    python flexigis_simulate.py

Simulates urban energy requirement using abstracted dataset

- drop_database::

    dropdb --username=$(postgres_user) --port=$(postgres_port) --host=$(postgres_host) $(postgres_database)

Provides option to delete or retain database

- example::

    python example.py
    python plot_polygons.py
    python flexigis_simulate.py

Runs a test example data abstraction and simulation using filtered OSM data stored as csv file

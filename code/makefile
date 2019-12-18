###################################################################################
#   FlexiGIS                                                                      #
#                                                                                 #
#   Copyright "2020" "DLR VE"                                                     #
#										  #
#   Licensed under the BSD-3-Clause, "New BSD License" or "Modified BSD License"  #
#                                                                                 #
#   Redistribution and use in source and binary forms, with or without            #
#   modification, are permitted provided that the following conditions are met:   #
#                                                                                 #
#   1. Redistributions of source code must retain the above copyright notice,     #
#      this list of conditions and the following disclaimer.                      #
#                                                                                 #
#   2. Redistributions in binary form must reproduce the above copyright notice,  #
#      this list of conditions and the following disclaimer in the documentation  #
#      and/or other materials provided with the distribution.                     #
#                                                                                 #
#   3. Neither the name of the copyright holder nor the names of its contributors #
#      may be used to endorse or promote products derived from this software      #
#      without specific prior written permission.                                 #
#                                                                                 #
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"   #
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE     #
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE#
#   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE  #
#   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL    #
#   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR    #
#   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER    #
#   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, #
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE #
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.          #
#                                                                                 #
#        https://opensource.org/licenses/BSD-3-Clause                             #
###################################################################################


#=================================================================================#
#              Setting the config file                                            #
#=================================================================================#

config:=config.mk
include $(config)

#=================================================================================#
#              Output Files                                                       #
#=================================================================================#
ROAD_CSV:= $(load_folder)/highway.csv
BUILDINGS_CSV:=$(output_folder)/buildings.csv
#=================================================================================#
#              Definition of tasks                                                #
#=================================================================================#


.PHONY: all
.PHONY: download
.PHONY: filter_data
.PHONY: export_data
.PHONY: abstract_data
.PHONY: demand_supply_simulation
.PHONY: drop_database

#=================================================================================#
#              Environment Variables                                              #
#=================================================================================#

all: drop_database download filter_data export_data abstract_data demand_supply_simulation

#=================================================================================#
#              DOWNLOAD OSM DATASETS                                              #
#=================================================================================#


# Step1: Download the OSM raw geo urban data.

download:
	@echo "\n### Step1 ### \nDownload the OSM raw data from \n   '$(OSM_raw_data_URL)' \n and saving it to \n   '$(OSM_raw_data)':"
	@date >> log/download.log
	wget -nv -O $(OSM_raw_data) $(OSM_raw_data_URL) >> log/download.log 2>&1
	@echo "Done. Download OSM raw data" >> log/download.log
	#@date >> log/download.log
	@echo "--> Done. Download OSM raw data."
#=================================================================================#
#              BUILDING LANDUSE HIGHWAYS DATA EXTRACTION                          #
#=================================================================================#

# Step2: Filtering the OSM raw urban data.

filter_data:
	@echo "\n### Filtering the OSM raw geo-urban datasets:"
	@date >> log/osmosis.log
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
	--write-pbf file=$(OSM_merged_data) >> log/osmosis.log 2>&1;
	@echo "osmosis data filtering done." >> log/osmosis.log
	@date >> log/osmosis.log
	@echo "--> Done. OSM filtered urban energy infrastructure"

#=================================================================================#
#              URBAN DATA EXPORT TO DATABASE                                      #
#=================================================================================#

# Step3: Export the Filtered OSM data to the Postgres Server.

export_data:
	@echo "\n### Step3 ### \nExporting the Filtered OSM data to Postgres Server:"
	@date >> log/database.log
	export PGPASSWORD=$(postgres_password); createdb -U $(postgres_user) -h $(postgres_host) $(postgres_database);
	export PGPASSWORD=$(postgres_password); $(osm2pgsql_bin) -r pbf --username=$(postgres_user) --database=$(postgres_database) --host=$(postgres_host) --port=$(postgres_port) -s \
	-C $(osm2pgsql_cache) --hstore --number-processes $(osm2pgsql_num_processes) $(OSM_merged_data);
	#@touch log/database_import.done
	@echo "OSM data export to database done." >> log/database.log
	@date >> log/osm2pgsql.log
	#@date >> log/database.log
	@echo "--> Done. FlexiGIS OSM data Export."

#=================================================================================#
#              ABSTRACTION AND DATA PROCESSING                                    #
#=================================================================================#

# Step4: Execute the abstraction script flexigis_buildings.py & flexigis_road.py on the database created in Step3

abstract_data:
	@echo "\n### Step4 ### \nRunning the abstraction script flexigis_road.py on the database '$(postgres_database)':"
	# log/abstraction.done: log/database_import.done
	@date >> log/abstract.log
	@if [ $(postgres_password) =  ]; \
	then \
	python flexigis_road.py -U $(postgres_user) -P $(postgres_port) -H $(postgres_host) -D $(postgres_database) ;\
	else \
	python flexigis_road.py -U $(postgres_user) -P $(postgres_port) -H $(postgres_host) -D $(postgres_database) -X $(postgres_password) ; \
	fi
	@echo "highway data abstraction done." >> log/abstract.log
	#@touch log/abstraction.done
	@echo "--> Done. FlexiGIS Highway Data Abstraction."
	@echo "\n### Step5 ### \nRunning the abstraction script flexigis_buildings.py on the database '$(postgres_database)':"
	@date >> log/abstract.log
	@if [ $(postgres_password) =  ]; \
	then \
	python flexigis_buildings.py -U $(postgres_user) -P $(postgres_port) -H $(postgres_host) -D $(postgres_database) ;\
	else \
	python flexigis_buildings.py -U $(postgres_user) -P $(postgres_port) -H $(postgres_host) -D $(postgres_database) -X $(postgres_password) ; \
	fi
	@echo "Building and landuse data abstraction done." >> log/abstract.log
	@echo "Generating plots."
	@if [ -e $(BUILDINGS_CSV) ]; then python plot_polygons.py ; fi
	@echo "plots for building and highway generated." >> log/abstract.log
	@echo "--> Done. FlexiGIS Buildings Data Abstraction."

#=================================================================================#
#              MODELLING URBAN ENERGY REQUIREMENT                                 #
#=================================================================================#

# Step5: Modelling urban energy requirements

demand_supply_simulation:
	@echo "\n### Step6 ### \nModelling demand and supply and saving aggregated energry required as CSV files to folder '$(load_folder)':"
	@date >> log/urban_energy.log
	@if [ -e $(ROAD_CSV) ]; then python flexigis_urban_energy_requirments.py ; fi
	@echo "Done. Modelling urban energy requirements." >> log/urban_energy.log
	@echo "--> Done. Modelling urban energy requirements"

#=================================================================================#
#              DROPPING                                                           #
#=================================================================================#

# If you wish to drop your database

drop_database:
	$(eval answer := $(shell read -r -p "Do you really want to delete the FlexiGIS database '$(postgres_database)'? Type 'yes' if you are sure you wish to continue: " ANSWER; echo $$ANSWER))
	@if [ "$(answer)" = "yes" ]; then if(dropdb --username=$(postgres_user) --port=$(postgres_port) --host=$(postgres_host) $(postgres_database)); then echo "The FlexiGIS database '$(postgres_database)' has been dropped."; fi else echo "\nDid not drop the FlexiGIS database '$(postgres_database)'."; fi

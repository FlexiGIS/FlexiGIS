"""**Example using filtered OSM building and highway data stored as csv file**."""
import pandas as pd
import flexigis_buildings
import flexigis_road

# get logging
flexigis_road.logging

# read in filtered OSM csv files.
csv_file = "../data/01_raw_input_data/example_OSM_data/"
df_road = pd.read_csv(csv_file+"OSM_road.csv")
df_building = pd.read_csv(csv_file+"OSM_building.csv")

flexigis_road.flexiGISroad(df_road)
flexigis_buildings.flexiGISbuilding(df_building)

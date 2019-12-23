"""Example using filtered OSM building data stored as csv file."""
import pandas as pd
import flexigis_buildings

csv_file = "../data/01_raw_input_data/"
df = pd.read_csv(csv_file+"OSM_data.csv")
flexigis_buildings.flexiGISbuilding(df)

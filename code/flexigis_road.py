"""Module I.

Get Highway data from database and export result csv files.
"""
import pandas as pd
from db_connect import dbconn_from_args
import logging
import os
from pathlib import Path

from flexigis_utils import (compute_area, data_to_csv)

# create a log file
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/flexigis_road.log",
                    level=logging.DEBUG)


if Path("../data/02_urban_output_data/").exists():
    logging.info("directory {} already exists.".
                 format("02_urban_output_datas"))
    pass
else:
    os.mkdir("../data/02_urban_output_data/")
    logging.info("directory {} succesfully created!.".
                 format("02_urban_output_datas"))


class Roads:
    """Object class that get line data from database and export output to csv.

    get_table_from_db: Connect to data base and query database returns a
    pandas dataframe.
    get_features: Calculates roads length and area, and exports dataframe
    to a csv file.
    """

    def get_table_from_db(self, cur, conn):
        """Extract database table."""
        self.cur = cur
        self.conn = conn
        self.table = "planet_osm_line"
        self.ways_column = "highway"
        self.destination = "../data/02_urban_output_data/"
        # Queryy database
        # Convert postgres encoded geometric projection to EPSG:3857 format
        # EPSG:3857 is a Spherical Mercator projection coordinate system
        # popularized by web services such as Google and later OpenStreetMap.
        # https://wiki.openstreetmap.org/wiki/EPSG:3857
        sql = "SELECT osm_id, highway,\
        way, ST_Length(ST_Transform(way, 3857)) as l,\
         ST_ASEWKT(ST_Transform(way, 3857)) as p FROM planet_osm_line"

        self.cur.execute(sql)
        self.rows = self.cur.fetchall()
        # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=[
            "osm_id", self.ways_column,
            "geometry", "length", "polygon_1"])
        self.data = self.df.dropna().sort_values(by="highway")
        return self.data

    # get features from dataframe
    def get_features(self, dataset):
        """Get OSM High way features."""
        self.highway_feature = ['motorway', 'primary',
                                'residential', 'secondary',
                                'tertiary', 'trunk', 'unclassified']
        self.width = [11.5, 6.5, 5.5, 7.5, 6.5, 7.5, 6.5]
        self.dataset = dataset.loc[dataset["highway"].
                                   isin(self.highway_feature)]
        self.new_data_ = self.dataset.set_index(["highway"])
        self._width_ = dict(zip(self.highway_feature, self.width))
        # compute area and save data to csv
        new_data = compute_area(self.new_data_, self._width_)
        logging.info("Roads area calculation done!")
        return data_to_csv(new_data, self.destination+self.ways_column+".csv")


if __name__ == "__main__":
    conn = dbconn_from_args()
    cur = conn.cursor()
    roads = Roads()
    data = roads.get_table_from_db(cur, conn)
    roads.get_features(data)
    logging.info("Extraction of osm_id, higway, length, and geometry and area")
    print("Done. Highway data abstracted!")
    logging.info("FlexiGIS Highway job done.!")

"""**Get georeferenced Highway data from database**.

Highway categories such as motor ways, squares, bus stop, links. Outputs are
 exported to csv files.
"""
import pandas as pd
import logging
import os
from pathlib import Path

from db_connect import dbconn_from_args
from flexigis_utils import (compute_area, data_to_file)
# create a log file
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/flexigis_road.log",
                    level=logging.DEBUG)


class Roads:
    """Get highway data from database.

    - Example::

        from db_connect import dbconn_from_args # db_connect.py in code dir.

        conn = dbconn_from_args() # connection to database
        cur = conn.cursor()
        roads = flexigis_road.Roads() # instanciate the Road class
        data = roads.get_road_from_db(cur, conn) # get roads data from database

    """

    def __init__(self):
        """Init method that hold needed variables."""
        self.table = "planet_osm_line"
        self.ways_column = "highway"
        self.destination = "../data/02_urban_output_data/"
        if Path(self.destination).exists():
            logging.info("directory {} already exists.".
                         format(self.destination))
            pass
        else:
            os.mkdir(self.destination)
            logging.info("directory {} succesfully created!.".
                         format(self.destination))

    def get_road_from_db(self, cur, conn):
        """Extract database table.

        :param object cur: data base cursor
        :param object conn: database connection
        :return: dataframe of  OSM highway data for lines
        :rtype: DataFrame
        """
        self.cur = cur
        self.conn = conn

        # self.destination = "../data/02_urban_output_data/"
        # Queryy database
        # Convert postgres encoded geometric projection to EPSG:3857 format
        # EPSG:3857 is a Spherical Mercator projection coordinate system
        # popularized by web services such as Google and later OpenStreetMap.
        # https://wiki.openstreetmap.org/wiki/EPSG:3857
        sql = "SELECT osm_id, highway,\
        ST_Length(ST_Transform(way, 3857)) as l,\
            ST_ASEWKT(ST_Transform(way, 3857)) as p FROM planet_osm_line"

        self.cur.execute(sql)
        self.rows = self.cur.fetchall()
        # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=[
            "osm_id", self.ways_column, "length", "geometry"])
        self.data = self.df.dropna().sort_values(by="highway")
        return self.data

    # get features from dataframe
    def get_road_features(self, dataset):
        """Get OSM High way features.

        :param DataFrame dataset: highway dataset
        :return: csv containing highway attributes (eg. OSM_id, length, area)
        """
        self.highway_feature = ['motorway', 'primary',
                                'residential', 'secondary',
                                'tertiary', 'trunk', 'unclassified']
        self.width = [11.5, 6.5, 5.5, 7.5, 6.5, 7.5, 6.5]
        self.dataset = dataset.loc[dataset["highway"].
                                   isin(self.highway_feature)]
        self.new_data_ = self.dataset.set_index([self.ways_column])
        self._width_ = dict(zip(self.highway_feature, self.width))
        # compute area and save data to csv
        new_data = compute_area(self.new_data_, self._width_)
        logging.info("Highway area calculation done!")
        data_to_file(new_data, self.destination+self.ways_column)
        # data_to_csv(new_data, self.destination+self.ways_column+".csv")

    def get_road_features2(self, dataset):
        """Get Additional OSM Highway features, eg. motor_link, living_street.

        :param DataFrame dataset: highway dataset
        :return: csv containing highway attributes (eg. OSM_id, length, area)
        """
        self.highway_feature2 = ['living_street', 'motorway', 'pedestrian',
                                 'primary', 'secondary', 'service', 'tertiary',
                                 'trunk', 'motorway_link', 'primary_link',
                                 'secondary_link', 'tertiary_link',
                                 'trunk_link']
        self.width = [7.5, 15.50, 7.5, 10.5, 9.5, 7.5, 9.5, 9.5, 6.5, 6.5,
                      6.5, 6.5, 6.5]
        self.dataset = dataset.loc[dataset[self.ways_column].
                                   isin(self.highway_feature2)]
        self.new_data_ = self.dataset.set_index([self.ways_column])
        self._width_ = dict(zip(self.highway_feature, self.width))
        # compute area and save data to csv
        new_data = compute_area(self.new_data_, self._width_)
        logging.info("csv file of highway properties generated.")
        data_to_file(new_data, self.destination+self.table)


# TODO: Test newly added class and methods
class GetRoadsPolygons:
    """Gets highway polygons from database and export output to csv."""

    def __init__(self):
        """Init method that holds needed variables."""
        self.table = "planet_osm_highway_polygon"
        self.ways_column = "highway"
        self.destination = "../data/02_urban_output_data/"
        if Path(self.destination).exists():
            logging.info("directory {} already exists.".
                         format(self.destination))
            pass
        else:
            os.mkdir(self.destination)
            logging.info("directory {} succesfully created!.".
                         format(self.destination))

    # See FlexiGIS-Light repo for the usage of this class
    def get_roadpolygons_from_db(self, cur, conn):
        """Query database and return data as dataframe.

        :param object cur: data base cursor
        :param object conn: database connection
        :return: dataframe of  OSM highway data for polygons
        :rtype: DataFrame
        """
        # fetch high way column from db (line table)
        self.cur = cur
        self.conn = conn

        sql = "SELECT osm_id, highway, ST_Area(ST_Transform(way, 3857)) a,\
         ST_ASEWKT(ST_Transform(way, 3857))as p FROM planet_osm_polygon"

        self.cur.execute(sql)
        self.rows = self.cur.fetchall()

        # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=[
            "osm_id", self.ways_column,
            "area", "geometry"])
        self.data = self.df.dropna().sort_values(by="highway")
        return self.data
        logging.info("polygon properties for highway extracted from database.")

    # get features from dataframe
    def get_roadpolygons_features(self, dataset):
        """Get OSM High way features.

        :param DataFrame dataset: highway dataset
        :return: csv containing highway attributes (eg. OSM_id, area, geometry)
        """
        self.destination = "../data/02_urban_output_data/"
        self.roadpolygons_feature = ['crossing', 'footway', 'living_street',
                                     'pedestrian', 'platform', 'residential',
                                     'service', 'traffic_island']
        self.dataset = dataset.loc[dataset["highway"].
                                   isin(self.roadpolygons_feature)]
        self.new_data_polygons = self.dataset.set_index(["highway"])

        data_to_file(self.new_data_polygons,
                     self.destination+self.table)
        logging.info("csv file for polygons generated.")


class GetPoints:
    """Gets highway data for points(Nodes) from database."""

# See FlexiGIS-Light repo for the usage of this class
    def __init__(self):
        """Init method that holds needed variables."""
        self.table = "planet_osm_highway_point"
        self.ways_column = "highway"
        self.destination = "../data/02_urban_output_data/"
        if Path(self.destination).exists():
            logging.info("directory {} already exists.".
                         format(self.destination))
            pass
        else:
            os.mkdir(self.destination)
            logging.info("directory {} succesfully created!.".
                         format(self.destination))

    def get_point_from_db(self, cur, conn):
        """Extract database table.

        :param object cur: data base cursor
        :param object conn: database connection
        :return: dataframe of  OSM highway data for points
        :rtype: DataFrame
        """
        # fetch high way column from db (line table)
        self.cur = cur
        self.conn = conn

        # query database
        sql = "SELECT osm_id, highway,ST_ASEWKT(ST_Transform(way, 3857))as p,\
         ST_X(ST_Transform (way, 3857)) as Longitude,\
          ST_Y(ST_Transform(way, 3857)) as Latitude FROM planet_osm_point"

        self.cur.execute(sql)
        self.rows = self.cur.fetchall()

        # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=[
            "osm_id", self.ways_column, "geometry", "Longitude", "Latitude"])
        self.data = self.df.dropna().sort_values(by=self.ways_column)
        return self.data
        logging.info("node properties for highway extracted from database.")
        # get features from dataframe

    def get_point_features(self, dataset):
        """Get OSM High way features.

        :param DataFrame dataset: highway dataset
        :return: csv containing highway attributes (eg. OSM_id, geometry)
        """
        self.point_feature = ['bus_stop', 'crossing', 'give_way',
                              'motorwyay_junction', 'passing_place',
                              'platform', 'speed_camera', 'stop',
                              'street_lamp', 'traffic_signals']
        self.dataset = dataset.loc[dataset[self.ways_column].
                                   isin(self.point_feature)]
        self.new_data_points = self.dataset.set_index([self.ways_column])

        data_to_file(self.new_data_points,
                     self.destination+self.table)
        logging.info("csv file for points generated.")


def flexiGISroad(data):
    """Execute `Roads` class.

    :param DataFrame data: OSM highway dataset

    This function can be imported as a module, for highway data abstraction.

    - Example::

        import pandas as pd
        import flexigis_road

        # get logging
        flexigis_road.logging
        csv_file = "../data/01_raw_input_data/example_OSM_data/"
        df_road = pd.read_csv(csv_file+"OSM_road.csv") # filtered OSM data
        flexigis_road.flexiGISroad(df_road) # export abstracted highway data
    """
    roads = Roads()
    roads.get_road_features(data)
    logging.info("Extraction of osm_id, higway, length, and geometry and area")
    print("Done. Highway data abstracted!")
    logging.info("FlexiGIS Highway job done.!")


if __name__ == "__main__":
    print("  ==== FLEXIGIS HIGHWAY ====")
    conn = dbconn_from_args()
    cur = conn.cursor()
    roads = Roads()
    data = roads.get_road_from_db(cur, conn)
    flexiGISroad(data)

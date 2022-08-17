"""**Get building and landuse georeferenced data from database**.

Output georeferenced building data are categorized into Agricultural,
Commercial, Educational, Industrial and Residential. Outputs data are stored as
stored as csv files.
"""
import pandas as pd
import os
from pathlib import Path
import shutil
from geopandas import GeoDataFrame
from shapely import wkt
import logging

from flexigis_utils import dbconn_from_args
from flexigis_utils import (get_polygons, get_intersects, mask_landuse_data,
                            get_features, get_data_from_buildings,
                            get_csv_categories)
# create a log file
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/flexigis_buildings.log",
                    level=logging.DEBUG)


class BuildingPolygons:
    """Get landuse and building data from database."""

    def __init__(self):
        """Init method that holds needed variables."""
        self.table = "planet_osm_polygon"
        self.ways_building = "building"
        self.ways_landuse = "landuse"

    def get_building_landuse_polygons(self, cur, conn):
        """Connect to database and query table.

        :param object cur: data base cursor
        :param object conn: database connection
        :return: dataframe of OSM data for building and landuse
        :rtype: DataFrame
        """
        self.cur = cur
        self.conn = conn

    # fetch polygons (building and landuse) columns from db
        sql = "SELECT osm_id, building, landuse, \
        ST_Area(ST_Transform(way, 3857)) a,\
         ST_ASEWKT(ST_Transform(way, 3857))as p FROM planet_osm_polygon"
        self.cur.execute(sql)
        self.rows = self.cur.fetchall()

    # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=[
                               "osm_id", self.ways_building, self.ways_landuse,
                               "area", "polygon"])
        return self.df

    # Building data correction
    def get_building(self, df):
        """Get building data."""
        self.df_building = df.drop(columns=["landuse"])
        self.data_building = self.df_building.dropna().\
            sort_values(by="building")
        self.new_building = self.data_building["polygon"].\
            str.split(";", n=1, expand=True)
        self.data_building["geometry"] = self.new_building[1]
        self.data_building = self.data_building.drop(columns=["polygon"])

        # Building data to GeoDataFrame
        self.data_building['geometry'] = self.data_building['geometry'].\
            apply(wkt.loads)
        self.data_building = GeoDataFrame(self.data_building,
                                          geometry='geometry')
        self.data_building = self.data_building.set_index([self.ways_building])
        return self.data_building

    def get_unique_features(self, df):
        """Get unique features for data."""
        self.features_ = df.index.unique()
        return self.features_
        # print(features_building)

    def get_landuse(self, df):
        """Get landuse data."""
        # Landuse data correction
        self.df_landuse = df.drop(columns=[self.ways_building])
        self.data_landuse = self.df_landuse.dropna().\
            sort_values(by=self.ways_landuse)
        self.new_landuse = self.data_landuse["polygon"]\
            .str.split(";", n=1, expand=True)
        self.data_landuse["geometry"] = self.new_landuse[1]
        self.data_landuse = self.data_landuse.drop(columns=["polygon"])
        # Landuse data to GeoDataFrame
        self.data_landuse['geometry'] = self.data_landuse['geometry'].\
            apply(wkt.loads)
        self.data_landuse = GeoDataFrame(self.data_landuse,
                                         geometry='geometry')
        self.data_landuse = self.data_landuse.set_index([self.ways_landuse])
        return self.data_landuse

        # features_landuse = data_landuse.index.unique()
        # print(features_landuse)


def get_data_from_db():
    """Get building and landuse as DataFrame from database.

    :return: dataset containing building and landuse columns
    :retype: DataFrame
    """
    conn = dbconn_from_args()
    cur = conn.cursor()
    polygons = BuildingPolygons()
    df = polygons.get_building_landuse_polygons(cur, conn)
    return df


def get_building_data(df):
    """Get building data as geodataframe.

    :param DataFrame df: Filtered OSM data from database
    :return: building dataset
    :retype: GeoDataFrame
    """
    polygons = BuildingPolygons()
    data_building = polygons.get_building(df)
    return data_building


def get_landuse_data(df):
    """Get landuse data as geodataframe.

    :param DataFrame df: Filtered OSM data from database
    :return: landuse dataset
    :retype: GeoDataFrame
    """
    polygons = BuildingPolygons()
    data_landuse = polygons.get_landuse(df)
    return data_landuse


def all_building_categories(df, data_building, data_landuse, main_destination,
                            temp_destination):
    """Output abstracted data for all categories.

    :param DataFrame df: Filtered OSM data
    :param DataFrame data_building: building data
    :param DataFrame data_landuse: landuse daa
    :param str main_destination: output data destination
    :param str temp_destination: temp data destination
    """
    # df = get_data_from_db()
    data_building = data_building
    polygons = BuildingPolygons()
    data_landuse = data_landuse
    features_building = polygons.get_unique_features(data_building)

    # create temp directory to store temporary csv files
    if Path(temp_destination).exists():
        logging.info("directory {} already exists.".
                     format(str(temp_destination)))
        pass
    else:
        os.mkdir(temp_destination)
        logging.info("directory {} succesfully created!".
                     format(str(temp_destination)))

    print("INFO: Extracting building and landuse intersects")

    # Landuse categories of interest
    classifications = [
        "commercial", "retail", "residential", "farmland", "farmyard",
        "industrial"
    ]

    for building_type in features_building:
        # print("getting intersects for %s" % building_type)
        _building_type_ = get_polygons(data_building, str(building_type))
        intersects = get_intersects(_building_type_, data_landuse)
        if intersects.empty:
            continue

        mask_intersects = mask_landuse_data(data_landuse, intersects)
        for category in classifications:
            if category in mask_intersects.index:
                _category_ = get_features(mask_intersects, intersects,
                                          select=category)
                final_data = get_data_from_buildings(data_building, _category_)
                # print("getting dataframe for %s" % category)

                # write output to csv file
                final_data.to_csv(temp_destination + category+"_" +
                                  building_type+".csv", encoding="utf8")
                logging.info("csv file for {} succesfuly created in temp.".
                             format(str(building_type)))


def commercial_buildings(temp_destination):
    """Extract commercial buildings (commercial + retial polygons).

    :param str temp_destination: temp directory path
    :return: DataFrame containing commercial buildings
    :retype: DataFrame
    """
    commercials_comm = get_csv_categories(temp_destination, "commercial")
    commercials_retail = get_csv_categories(temp_destination, "retail")
    commercial = pd.concat([commercials_comm, commercials_retail])
    listOfString_comm = ['commercial' for i in range(len(commercial))]
    commercial.insert(1, "buildings", listOfString_comm, True)
    commercial = commercial.reset_index(drop=True)
    return commercial


def residential_buildings(temp_destination):
    """Extract residential buildings.

    :param str temp_destination: temp directory path
    :return: DataFrame containing residential buildings
    :retype: DataFrame
    """
    residential = get_csv_categories(temp_destination, "residential")
    listOfString_res = ['residential' for i in range(len(residential))]
    residential.insert(1, "buildings", listOfString_res, True)
    residential = residential.reset_index(drop=True)
    return residential


def industrial_building(temp_destination):
    """Extract industrial buildings.

    :param str temp_destination: temp directory path
    :return: DataFrame containing industrial buildings
    :retype: DataFrame
    """
    industrial = get_csv_categories(temp_destination, "industrial")
    listOfString_ind = ['industrial' for i in range(len(industrial))]
    industrial.insert(1, "buildings", listOfString_ind, True)
    industrial = industrial.reset_index(drop=True)
    return industrial


def agricultural_building(temp_destination):
    """Extract agricultural (Farmland + Famyard polygons).

    :param str temp_destination: temp directory path
    :return: DataFrame containing agricultural buildings
    :retype: DataFrame
    """
    agriculture_farmyard = get_csv_categories(temp_destination, "farmyard")
    agriculture_farmland = get_csv_categories(temp_destination, "farmland")
    agriculture = pd.concat([agriculture_farmyard, agriculture_farmland])
    listOfString_agr = ['agricultural' for i in range(len(agriculture))]
    agriculture.insert(1, "buildings", listOfString_agr, True)
    agricultural = agriculture.reset_index(drop=True)
    return agricultural


def educational_building(data):
    """Extract educational.

    :param Dataframe data: Pandas Dataframe of building dataset
    :return: DataFrame containing educational buildings
    :retype: DataFrame
    """
    education = data.loc[["kindergarten", "school", "university"], :]
    listOfString_edu = ['educational' for i in range(len(education))]
    education.insert(1, "buildings", listOfString_edu, True)
    educational = education.reset_index(drop=True)
    return educational


def save_categorized_to_file(temp_destination, main_destination, *argv):
    """Export categorized buildings of interest to shape file.

    :param str temp_destination: directory path to store temp file
    :param str main_destination: directory path to store output data
    :param DataFrame argv: pandas dataframe of abstracted data
    """
    # clean ../02_urban_output_data/temp/ directory
    # inspired by question from stackoverflow
    # https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
    folder = temp_destination
    main_destination = main_destination
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            logging.info("../data/temp directory cleaned.")

        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            logging.error('Failed to delete %s. Reason: %s' % (file_path, e))

    # write categories to csv/shapefile files separately
    for arg in argv:
        print("INFO: shape file for"+" "+str(arg.buildings[0]))
        # arg.to_csv(main_destination+str(arg.buildings[0])+".csv",
        #            encoding="utf8")
        arg.to_file(main_destination+str(arg.buildings[0]),
                    driver='ESRI Shapefile')
        logging.info("{} csv file generated succesfuly.".
                     format(str(arg.buildings[0])))


def flexiGISbuilding(df):
    """Execute all functions.

    :param DataFrame data: OSM building dataset

    This function can be imported as a module, for buildings data extraction.

    - Example::

        import pandas as pd
        import flexigis_buildings

        # get logger
        flexigis_buildings.logging
        csv_file = "../data/01_raw_input_data/example_OSM_data/"
        # filtered OSM data
        df_building = pd.read_csv(csv_file+"OSM_building.csv")
        # export extracted building data as csv file
        flexigis_buildings.flexiGISbuilding(df_building)
    """
    # csv files destination
    temp_destination = "../data/02_urban_output_data/temp/"
    main_destination = "../data/02_urban_output_data/"
    data_building = get_building_data(df)
    data_landuse = get_landuse_data(df)
    all_building_categories(df, data_building, data_landuse, main_destination,
                            temp_destination)
    commercial = commercial_buildings(temp_destination)
    residential = residential_buildings(temp_destination)
    industrial = industrial_building(temp_destination)
    agricultural = agricultural_building(temp_destination)
    educational = educational_building(data_building)
    all_df = pd.concat([agricultural, commercial, educational, industrial,
                        residential], ignore_index=True)

    # save landuse data to file
    # data_landuse.to_csv(main_destination+"landuse.csv", encoding="utf8")
    data_landuse.reset_index().to_file(main_destination+"landuse", driver='ESRI Shapefile')
    # Building data
    # all_df.to_csv(main_destination+"buildings.csv", encoding="utf8")
    all_df.to_file(main_destination+"buildings", driver='ESRI Shapefile')

    save_categorized_to_file(temp_destination, main_destination, commercial,
                             residential, industrial, agricultural,
                             educational)
    print("Done. shape files of categorised building generated!")
    if os.path.isdir(temp_destination):
        shutil.rmtree(temp_destination)
    logging.info("FlexiGIS building job done.!")


if __name__ == "__main__":
    print("  ==== FLEXIGIS BUILDINGS ====")
    df = get_data_from_db()
    flexiGISbuilding(df)

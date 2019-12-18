"""Module I.

Get Building and Landuse data from database and export results to CSV.
"""
import pandas as pd
from db_connect import dbconn_from_args
import os
from pathlib import Path
import shutil
from geopandas import GeoDataFrame
from shapely import wkt
import logging

from flexigis_utils import (get_polygons, get_intersects, mask_landuse_data,
                            get_features, get_data_from_buildings,
                            get_csv_categories)

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/flexigis_buildings.log",
                    level=logging.DEBUG)

# csv files destination
temp_destination = "../data/02_urban_output_data/temp/"
main_destination = "../data/02_urban_output_data/"


class BuildingPolygons:
    """Object class that gets landuse and building data from database.

    get_building_landuse_polygons: returns querried database table as pandas
    dataframe.
    get_building: return GeoDataFrame for building categories
    get_unique_features: return a list of uniques categories of landuse or
    building.
    get_landuse: returns a GeoDataFrame for landuse categories.
    """

    def get_building_landuse_polygons(self, cur, conn):
        """Connect to database and query table."""
        self.cur = cur
        self.conn = conn
        self.table = "planet_osm_polygon"
        self.ways_building = "building"
        self.ways_landuse = "landuse"

    # fetch polygons (building and landuse) columns from db
        sql = "SELECT osm_id, building, landuse, way, way_area,\
        ST_Area(ST_Transform(way, 3857)) a,\
         ST_ASEWKT(ST_Transform(way, 3857))as p FROM planet_osm_polygon"
        self.cur.execute(sql)
        self.rows = self.cur.fetchall()

    # save selected columns as pandas dataframe
        self.df = pd.DataFrame(self.rows, columns=[
                               "osm_id", "building", "landuse", "geometry",
                               "way_area", "area", "polygon"])
        return self.df
        # Building data correction

    def get_building(self, df):
        """Get building columns.

        df: pandas dataframe
        """
        self.df_building = df.drop(columns=["landuse", "geometry", "way_area"])
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
        self.data_building = self.data_building.set_index(["building"])
        return self.data_building

    def get_unique_features(self, df):
        """Get unique features for data."""
        self.features_ = df.index.unique()
        return self.features_
        # print(features_building)

    def get_landuse(self, df):
        """Get landuse column."""
        # Landuse data correction
        self.df_landuse = df.drop(columns=["building", "geometry", "way_area"])
        self.data_landuse = self.df_landuse.dropna().sort_values(by="landuse")
        self.new_landuse = self.data_landuse["polygon"]\
            .str.split(";", n=1, expand=True)
        self.data_landuse["geometry"] = self.new_landuse[1]
        self.data_landuse = self.data_landuse.drop(columns=["polygon"])
        # Landuse data to GeoDataFrame
        self.data_landuse['geometry'] = self.data_landuse['geometry'].\
            apply(wkt.loads)
        self.data_landuse = GeoDataFrame(self.data_landuse,
                                         geometry='geometry')
        self.data_landuse = self.data_landuse.set_index(["landuse"])
        return self.data_landuse

        # features_landuse = data_landuse.index.unique()
        # print(features_landuse)


def get_data_from_db():
    """Get building and landuse as DataFrame from database."""
    conn = dbconn_from_args()
    cur = conn.cursor()
    polygons = BuildingPolygons()
    df = polygons.get_building_landuse_polygons(cur, conn)
    return df


def get_building_data():
    """Get building data as geodataframe."""
    polygons = BuildingPolygons()
    df = get_data_from_db()
    data_building = polygons.get_building(df)
    return data_building


def all_building_categories():
    """Output abstracted data for all categories."""
    df = get_data_from_db()
    polygons = BuildingPolygons()
    data_building = polygons.get_building(df)
    data_landuse = polygons.get_landuse(df)
    features_building = polygons.get_unique_features(data_building)

    # save landuse data to csv
    data_landuse.to_csv(main_destination+"landuse.csv", encoding="utf8")
    # create temp directory to store temporary csv files
    if Path(temp_destination).exists():
        pass
    else:
        os.mkdir(temp_destination)

    print("Extracting building and landuse intersects!")

    for building_type in features_building:
        # print("getting intersects for %s" % building_type)
        _building_type_ = get_polygons(data_building, str(building_type))
        intersects = get_intersects(_building_type_, data_landuse)
        mask_intersects = mask_landuse_data(data_landuse, intersects)
        # Landuse categories of interest
        classifications = ["commercial", "retail", "residential", "farmland",
                           "farmyard", "industrial"]
        for category in classifications:
            if category in mask_intersects.index:
                _category_ = get_features(mask_intersects, intersects,
                                          select=category)
                final_data = get_data_from_buildings(data_building, _category_)
                # print("getting dataframe for %s" % category)

                # write output to csv file
                final_data.to_csv(temp_destination + category+"_" +
                                  building_type+".csv", encoding="utf8")


def commercial_buildings():
    """Extract commercial buildings (commercial + retial polygons)."""
    commercials_comm = get_csv_categories(temp_destination, "commercial")
    commercials_retail = get_csv_categories(temp_destination, "retail")
    commercial = pd.concat([commercials_comm, commercials_retail])
    listOfString_comm = ['commercial' for i in range(len(commercial))]
    commercial.insert(1, "buildings", listOfString_comm, True)
    commercial = commercial.reset_index(drop=True)
    return commercial


def residential_buildings():
    """Extract residential buildings."""
    residential = get_csv_categories(temp_destination, "residential")
    listOfString_res = ['residential' for i in range(len(residential))]
    residential.insert(1, "buildings", listOfString_res, True)
    residential = residential.reset_index(drop=True)
    return residential


def industrial_building():
    """Extract industrial buildings."""
    industrial = get_csv_categories(temp_destination, "industrial")
    listOfString_ind = ['industrial' for i in range(len(industrial))]
    industrial.insert(1, "buildings", listOfString_ind, True)
    industrial = industrial.reset_index(drop=True)
    return industrial


def agricultural_building():
    """Extract agricultural (Farmland + Famyard polygons)."""
    agriculture_farmyard = get_csv_categories(temp_destination, "farmyard")
    agriculture_farmland = get_csv_categories(temp_destination, "farmland")
    agriculture = pd.concat([agriculture_farmyard, agriculture_farmland])
    listOfString_agr = ['agricultural' for i in range(len(agriculture))]
    agriculture.insert(1, "buildings", listOfString_agr, True)
    agricultural = agriculture.reset_index(drop=True)
    return agricultural


def educational_building(data):
    """Extract educational."""
    education = data.loc[["kindergarten", "school", "university"], :]
    listOfString_edu = ['educational' for i in range(len(education))]
    education.insert(1, "buildings", listOfString_edu, True)
    educational = education.reset_index(drop=True)
    return educational


def save_categorized_to_csv_(*argv):
    """Export categorized buildings of interest to csv."""
    # clean ../02_urban_output_data/temp/ directory
    # inspired by question from stackoverflow
    # https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
    folder = temp_destination
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # write categories to csv files separately
    for arg in argv:
        arg.to_csv(main_destination+str(arg.buildings[0])+".csv",
                   encoding="utf8")


def main():
    """Execute all functions."""
    data_building = get_building_data()
    all_building_categories()
    commercial = commercial_buildings()
    residential = residential_buildings()
    industrial = industrial_building()
    agricultural = agricultural_building()
    educational = educational_building(data_building)
    all_df = pd.concat([agricultural, commercial, educational, industrial,
                        residential], ignore_index=True)
    all_df.to_csv(main_destination+"buildings.csv", encoding="utf8")

    save_categorized_to_csv_(commercial, residential, industrial,
                             agricultural, educational)
    print("Done. csv files of categorised building generated!")


if __name__ == "__main__":
    main()

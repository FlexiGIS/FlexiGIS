"""**Helper functions for FlexiGIS data abstraction**."""

import pandas as pd
import geopandas as gpd
import glob
from natsort import natsorted
from shapely import wkt
from geopandas import GeoDataFrame


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Helper functions flexigis_road
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def compute_area(dataset, width):
    """Compute area for each line feature and return a dataframe object.

    :param DataFrame dataset: OSM planet data
    :param dict width: unique highway category as `key` and the width in meters
     as the `value`
    :return: dataframe containing an "area" attribute
    :rtype: DataFrame
    """
    Area = []
    for key, value in width.items():
        area = dataset.loc[key]["length"]*value
        Area.append(area)

    if isinstance(Area[0], pd.Series) is True:
        Area = pd.concat(Area)
        dataset["area"] = Area.values
    else:
        dataset["area"] = Area

    dataset_new = dataset.reset_index()
    return dataset_new


def data_to_csv(dataset, name="name"):
    """Write a dataframe to a csv file.

    :param DataFrame dataset: OSM planet data
    :param str name: file name of the output csv file (eg. `table_name`)
    :return: csv file for highway category
    :rtype: csv file
    """
    dataset_new = dataset["geometry"].str.split(";", n=1, expand=True)
    dataset["polygon"] = dataset_new[1]
    dataset = dataset.drop(columns=["geometry"])
    dataset = dataset.rename(columns={"polygon": "geometry"})
    return dataset.to_csv(name, encoding="utf-8")


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# helper functions flexigis_buildings
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def get_polygons(data, select="feature"):
    """Get building classification.

    :param DataFrame data: OSM planet data
    :param str select: building data feature (eg. `apartment`, `farmhouse`)
    :return: GeoDataFrame of building category type
    :rtype: pandas.GeoDataFrame
    """
    _data_ = data.loc[select]
    if isinstance(_data_, pd.DataFrame) is True:
        return _data_

    elif isinstance(_data_, pd.DataFrame) is False:
        _data2_ = data.loc[[select]]
        return _data2_


# get intersection between building (yes) and landuse polygons
def get_intersects(data_building, data_landuse):
    """Get intersects for between building category and landuse.

    :param GeoDataFrame data_building: building data
    :param GeoDataFrame data_landuse: landuse data
    :return: GeoDataFrame of intersects between landuse and building.
    :rtype: pandas.GeoDataFrame
    """
    res_intersects = gpd.overlay(data_building, data_landuse,
                                 how="intersection")
    return res_intersects


def mask_landuse_data(data_landuse, res_intersects):
    """Mask intersections with landuse data.

    :param GeoDataFrame data_landuse: landuse data
    :param GeoDataFrame res_intersects: intersect between building and landuse
    :return: GeoDataFrame of building/landuse intersects.
    :rtype: pandas.GeoDataFrame
    """
    mask_landuse = data_landuse[data_landuse.osm_id.
                                isin(res_intersects.osm_id_2)]

    return mask_landuse


def get_features(mask_landuse, res_intersects, select="category"):
    """Get features polygons.

    :param GeoDataFrame mask_landuse: categories of building based on landuse
    :param GeoDataFrame res_intersects: intersect between building and landuse
    :return: GeoDataFrame of building/landuse intersects.
    :rtype: pandas.GeoDataFrame
    """
    mask_landuse = mask_landuse.loc[select]

    if isinstance(mask_landuse["osm_id"], pd.Series) is True:
        mask_data = res_intersects[res_intersects.osm_id_2.
                                   isin(mask_landuse["osm_id"])]
        return mask_data
    elif isinstance(mask_landuse["osm_id"], pd.Series) is False:
        mask_data = res_intersects[res_intersects.osm_id_2.
                                   isin(mask_landuse[["osm_id"]])]

        return mask_data


# mask_data from buildings
def get_data_from_buildings(data_building, mask_data):
    """Extract building for a landuse category.

    :param GeoDataFrame data_building: building data.
    :param GeoDataFrame mask_data: building/landuse intersects.
    :return: dataframe of buildings in a landuse category
    :rtype: pandas.DataFrame
    """
    slice_data = data_building[data_building.osm_id.
                               isin(mask_data["osm_id_1"])]
    return slice_data


def get_csv_categories(destination, name="category_name"):
    """Get csv files from a folder (temp folder).

    :param str destination: Path to categorised buildings csv files.
    :param str name: The name of building type based on landuse category.
    :return: dataframe of buildings in a landuse category
    :rtype: pandas.DataFrame
    """
    csv_categories = glob.glob(destination+name + "_*.csv")
    # sort csv  files
    csv_categories = natsorted(csv_categories)
    category = []
    for i in range(len(csv_categories)):
        data_category = pd.read_csv(csv_categories[i])
        category.append(data_category)
    category = pd.concat(category)
    category = category.set_index("building")
    # check if rows contain educational institutions (school, university,
    # kindergarten).
    educational = ["school", "university", "kindergarten"]
    mask = category[category.index.isin(educational)]
    # drop educationals in category
    category = category.drop(mask.index)
    return category

#
# def highway_to_geodata(df):
#     """Highway to geodata.
#
#     :param Dataframe df: georeferenced OSM data for lines.
#     :return: GeoDataFrame of highway OSM data
#     :rtype: pandas.GeoDataFrame
#     """
#     df["polygon"] = df["geometry"].apply(wkt.loads)
#     df = GeoDataFrame(df, geometry='polygon')
#     df = df.drop(columns=["geometry"])
#     return df


def df_to_geodata(df):
    """Convert data to geodataframe.

    :param Dataframe df: georeferenced OSM data for polygons.
    :return: GeoDataFrame of highway OSM data
    :rtype: pandas.GeoDataFrame
    """
    df['polygon'] = df['geometry'].apply(wkt.loads)
    df = GeoDataFrame(df, geometry='polygon')
    df = df.drop(columns=["geometry"])
    return df

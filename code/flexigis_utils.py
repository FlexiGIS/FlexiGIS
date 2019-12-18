"""Helper functions for FlexiGIS data abstraction."""
import pandas as pd
import geopandas as gpd
import glob
from natsort import natsorted


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Helper functions flexigis_road
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def compute_area(dataset, width):
    """Compute area for each line feature and return a dataframe object.

    dataset: Dataframe object
    width: Dictionary, unique highway category as key and the width in meters
    as value.
    """
    Area = []
    for key, value in width.items():
        area = dataset.loc[key]["length"]*value
        Area.append(area)
    Area = pd.concat(Area)
    dataset["area"] = Area.values
    dataset_new = dataset.reset_index()
    return dataset_new


def data_to_csv(dataset, name="name"):
    """Write data to csv file.

    dataset: dataframe object
    name: str object, name of the output csv file (the table name).
    """
    dataset_new = dataset["polygon_1"].str.split(";", n=1, expand=True)
    dataset["polygon"] = dataset_new[1]
    dataset = dataset.drop(columns=["polygon_1", "geometry"])
    return dataset.to_csv(name, encoding="utf-8")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# helper functions flexigis_buildings
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def get_polygons(data, select="feature"):
    """Get building classification.

    data: pandas dataframe
    selctect: string object (building category)
    """
    _data_ = data.loc[select]
    if isinstance(_data_, pd.DataFrame) is True:
        return _data_

    elif isinstance(_data_, pd.DataFrame) is False:
        _data2_ = data.loc[[select]]
        return _data2_


# get intersection between building (yes) and landuse polygons
def get_intersects(feature_data, data_landuse):
    """Get intersects for between building category and landuse.

    feature_data: GeoDataFrame of a particular building data_category
    data_landuse: GeoDataFrame of landuse
    """
    res_intersects = gpd.overlay(feature_data, data_landuse,
                                 how="intersection")
    return res_intersects


def mask_landuse_data(data_landuse, res_intersects):
    """Mask intersections with landuse data.

    Returns different landuse category for building.
    data_landuse: GeoDataFrame of landuse data
    res_intersects: intersects between landuse and building (GeoDataFrame)
    """
    mask_landuse = data_landuse[data_landuse.osm_id.
                                isin(res_intersects.osm_id_2)]

    return mask_landuse


def get_features(mask_landuse, res_intersects, select="category"):
    """Get features polygons.

    mask_landuse: GeoDataFrame of landuse category for buildings.
    Returns a landuse category for different buildings
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
    """Extract building for a particular landuse category."""
    slice_data = data_building[data_building.osm_id.
                               isin(mask_data["osm_id_1"])]
    return slice_data


def get_csv_categories(destination, name="category_name"):
    """Merge csv files in temp directory.

    Returns csv files of buildings based on landuse categories.
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

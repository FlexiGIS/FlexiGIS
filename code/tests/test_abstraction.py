"""Unittest for get_building script."""
# from pandas.util.testing import assert_frame_equal
import unittest
import pandas as pd
import flexigis_utils
from flexigis_buildings import BuildingPolygons
import numpy as np


class TestDataAbstraction(unittest.TestCase):
    """Unittest case."""

    def setUp(self):
        """SetUp."""
        Test_Input_Dir = "../data/01_raw_input_data/example_OSM_data/"
        test_file_name = "OSM_building.csv"
        test_road = "OSM_road.csv"

        try:
            df = pd.read_csv(Test_Input_Dir+test_file_name)
            df2 = pd.read_csv(Test_Input_Dir+test_road, index_col=False)

        except IOError:
            print("File cannot be read!")
        self.fixture = df
        self.fixture2 = df2
        self.polygon = BuildingPolygons()

    def test_get_building(self):
        """Test that the dataframe read in equals what you expect."""
        self.building_geodata = self.polygon.get_building(self.fixture)
        features_building = self.polygon\
            .get_unique_features(self.building_geodata)
        self.assertTrue(isinstance(self.building_geodata, pd.DataFrame))
        self.assertEqual(len(self.building_geodata.columns), 4)
        self.assertEqual(len(features_building),
                         len(self.building_geodata.index.unique()))
        self.assertIn("residential", features_building)

    def test_get_landuse(self):
        """Test that the dataframe read in equals what you expect."""
        self.landuse_geodata = self.polygon.get_landuse(self.fixture)
        self.assertTrue(isinstance(self.landuse_geodata, pd.DataFrame))
        self.assertTrue(len(self.landuse_geodata.columns), 4)

    def test_get_polygons(self):
        """Test DataFrame slicing of unique index elements."""
        data = self.polygon.get_building(self.fixture)
        self.building_type1 = flexigis_utils.get_polygons(data, "apartments")
        self.building_type2 = flexigis_utils.get_polygons(data, "barn")
        self.assertEqual(self.building_type1.index.unique(), ["apartments"])
        self.assertEqual(self.building_type2.index.unique(), ["barn"])

    def test_get_intersects(self):
        """Test intersects function between building and landuse."""
        self.landuse_geodata = self.polygon.get_landuse(self.fixture)
        data = self.polygon.get_building(self.fixture)
        self.building_type1 = flexigis_utils.get_polygons(data, "apartments")
        intersection = flexigis_utils.get_intersects(self.building_type1,
                                                     self.landuse_geodata)
        self.assertIn("area_1", intersection.columns)
        self.assertIn("area_2", intersection.columns)
        self.assertIn("osm_id_1", intersection.columns)
        self.assertIn("osm_id_2", intersection.columns)

    def test_mask_landuse_data(self):
        """Test land use mask from interest."""
        data = self.polygon.get_building(self.fixture)
        self.landuse_geodata = self.polygon.get_landuse(self.fixture)
        self.building_type1 = flexigis_utils.get_polygons(data, "apartments")
        intersection = flexigis_utils.get_intersects(self.building_type1,
                                                     self.landuse_geodata)
        mask_landuse = flexigis_utils.mask_landuse_data(self.landuse_geodata,
                                                        intersection)
        features_ = flexigis_utils.get_features(mask_landuse, intersection,
                                                select="commercial")
        final_data = flexigis_utils.get_data_from_buildings(data, features_)
        self.assertEqual(mask_landuse.index.name, "landuse")
        self.assertEqual(final_data.index.name, "building")
        self.assertEqual(len(np.unique(intersection.osm_id_2.values)),
                         len(np.unique(mask_landuse.osm_id.values)))

    # highway abstraction test
    def test_compute_area_small_data(self):
        """Test area calculation of road infrastructure."""
        highway_feature = ['motorway', 'primary', 'residential']
        dataset = self.fixture2.loc[self.fixture2["highway"].
                                    isin(highway_feature)]
        width_ = [11.5, 6.5, 5.5]
        width = dict(zip(highway_feature, width_))
        data_slice = dataset.iloc[[0, 300, 500], :]
        new_data = data_slice.set_index(["highway"])
        area_data = flexigis_utils.compute_area(new_data, width)
        self.assertIn("area", area_data)
        self.assertEqual(area_data["area"][0], area_data["length"]
                         [0]*width["motorway"])
        self.assertEqual(area_data["area"][1], area_data["length"]
                         [1]*width["primary"])
        self.assertEqual(area_data["area"][2], area_data["length"]
                         [2]*width["residential"])

    def test_compute_area_large_data(self):
        """Test computed area of road infrastructure for large data entry."""
        highway_feature = ['motorway', 'primary', 'residential']
        dataset = self.fixture2.loc[self.fixture2["highway"].
                                    isin(highway_feature)]
        width_ = [11.5, 6.5, 5.5]
        width = dict(zip(highway_feature, width_))
        new_data2 = dataset.set_index(["highway"])
        area_data2 = flexigis_utils.compute_area(new_data2, width)
        area_data2 = area_data2.set_index(["highway"])
        # print(area_data2.loc["motorway"]["length"]*width["motorway"])

        left = area_data2.loc["residential"]["area"]
        right = area_data2.loc["residential"]["length"]*width["residential"]
        self.assertIn("area", area_data2)
        pd.testing.assert_series_equal(left, right, check_names=False,
                                       check_exact=True)

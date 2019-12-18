"""Plot data using geopandas."""
from shapely import wkt
import pandas as pd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import seaborn as sns

csv_file = "../data/02_urban_output_data/"
buildings_csv = csv_file+"buildings.csv"
landuse_csv = csv_file+"landuse.csv"
highway_csv = csv_file+"highway.csv"
destination = "../data/04_Visualisation/"

df_building = pd.read_csv(buildings_csv, index_col=None)
df_highway = pd.read_csv(highway_csv, index_col=None)
df_landuse = pd.read_csv(landuse_csv, index_col=None)
classifications = ["commercial", "retail", "residential", "farmland",
                   "farmyard", "industrial"]
df_landuse = df_landuse.loc[df_landuse["landuse"].isin(classifications)]


def highway_to_geodata(df):
    """Highway to geodata."""
    df["polygon1"] = df["polygon"].apply(wkt.loads)
    df = GeoDataFrame(df, geometry='polygon1')
    df = df.drop(columns=["polygon"])
    return df


def df_to_geodata(df):
    """Convert data to geodataframe."""
    df['polygon'] = df['geometry'].apply(wkt.loads)
    df = GeoDataFrame(df, geometry='polygon')
    df = df.drop(columns=["geometry"])
    return df

def plot_building():
    """Plot polygons."""
    geodata_building = df_to_geodata(df_building)
    fig, ax = plt.subplots(1, figsize=(12, 10))
    geodata_building.plot(column='buildings', categorical=True, legend=True,
                          ax=ax, linewidth=0.1, cmap='Dark2',
                          edgecolor="0.8")
    leg = ax.get_legend()
    leg.set_title("building")
    leg.set_bbox_to_anchor((0.0, 0.05, 0.01, 0.8))
    plt.axis("off")
    plt.title("Building infrastructure in Oldenburg", fontsize=20)
    plt.savefig(destination+"buildings.png", dpi=300)

def plot_landuses():
    """Plot polygons."""
    geodata_building = df_to_geodata(df_building)
    geodata_landuse = df_to_geodata(df_landuse)
    fig, ax = plt.subplots(1, figsize=(12, 10))
    base = geodata_landuse.plot(column='landuse', categorical=True,
                                legend=True, ax=ax, linewidth=0.1,
                                cmap='tab10', edgecolor="0.8")
    geodata_building.plot(ax=base, edgecolor="0.8", color='white', legend=True)
    leg = ax.get_legend()
    leg.set_title("landuse")
    leg.set_bbox_to_anchor((0.0, 0.05, 0.01, 0.8))
    plt.axis("off")
    plt.title("Land use in Oldenburg", fontsize=20)
    plt.savefig(destination+"landuse.png", dpi=300)

def plot_roads():
    """Plot lines."""
    geodata_highway = highway_to_geodata(df_highway)
    fig, ax = plt.subplots(1, figsize=(12, 10))
    geodata_highway.plot(column='highway', categorical=True, legend=True,
                         ax=ax, linewidth=1, cmap='tab10', edgecolor="0.8")

    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor((0.0, 0.05, 0.01, 0.8))
    plt.title("Roads infrastructure in Oldenburg", fontsize=20)
    plt.axis("off")
    plt.savefig(destination+"highway.png", dpi=300)


if __name__ == "__main__":
    sns.set_style("dark")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
    plot_landuses()
    plot_roads()
    plot_building()

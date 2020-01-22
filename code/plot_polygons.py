"""**Plot data using geopandas**."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from flexigis_utils import (highway_to_geodata, df_to_geodata)

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


def plot_building(legend_box, fig_size, font_size, face_color):
    """Plot polygons for buildings.

    :param tuple(float) legend_box: tuple of floats, eg (0.0, 0.05, 0.01, 0.7)
    :param tuple(int) fig_size: figure size
    :param int font_size: title font size
    :param str face_color: backgroud color (eg, white, black)
    """
    geodata_building = df_to_geodata(df_building)
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata_building.plot(column='buildings', categorical=True, legend=True,
                          ax=ax, linewidth=0.1, cmap='Dark2',
                          edgecolor="0.8")

    ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("building")
    leg.set_bbox_to_anchor(legend_box)
    plt.axis("off")
    plt.title("Building infrastructure in Oldenburg", fontsize=font_size)
    plt.savefig(destination+"buildings.png", facecolor=fig.get_facecolor(),
                dpi=300)


def plot_landuses(legend_box, fig_size, font_size, face_color):
    """Plot polygons for landuse.

    :param tuple(float) legend_box: tuple of floats, eg (0.0, 0.05, 0.01, 0.7)
    :param tuple(int) fig_size: figure size
    :param int font_size: title font size
    :param str face_color: backgroud color (eg, white, black)
    """
    geodata_building = df_to_geodata(df_building)
    geodata_landuse = df_to_geodata(df_landuse)
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    base = geodata_landuse.plot(column='landuse', categorical=True,
                                legend=True, ax=ax, linewidth=0.1,
                                cmap='tab10', edgecolor="0.8")
    geodata_building.plot(ax=base, edgecolor="0.8", color='white', legend=True)

    ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("landuse")
    leg.set_bbox_to_anchor(legend_box)
    plt.axis("off")
    plt.title("Land use in Oldenburg", fontsize=font_size)
    plt.savefig(destination+"landuse.png", facecolor=fig.get_facecolor(),
                dpi=300)


def plot_roads(legend_box, fig_size, font_size, face_color):
    """Plot lines (highway).

    :param tuple(float) legend_box: tuple of floats, eg (0.0, 0.05, 0.01, 0.7)
    :param tuple(int) fig_size: figure size
    :param int font_size: title font size
    :param str face_color: backgroud color (eg, white, black)
    """
    geodata_highway = highway_to_geodata(df_highway)
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    geodata_highway.plot(column='highway', categorical=True, legend=True,
                         ax=ax, linewidth=1, cmap='tab10', edgecolor="0.8")

    ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Roads infrastructure in Oldenburg", fontsize=font_size)
    plt.axis("off")
    plt.savefig(destination+"highway.png", facecolor=fig.get_facecolor(),
                dpi=300)


if __name__ == "__main__":
    sns.set_style("dark")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
    legend_box = (0.0, 0.05, 0.01, 0.7)
    font_size = 15
    fig_size = (7, 5)
    face_color = "white"
    plot_landuses(legend_box, fig_size, font_size, face_color)
    plot_roads(legend_box, fig_size, font_size, face_color)
    plot_building(legend_box, fig_size, font_size, face_color)

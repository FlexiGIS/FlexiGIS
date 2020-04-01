"""**Plot georeferenced data (landuse, building, highway) using geopandas**."""
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


def plot_building(df_building, legend_box, fig_size, font_size, face_color,
                  destination):
    """Plot polygons for buildings.

    :param DataFrame df_building: building georeferenced data (geodataframe)
    :param tuple(float) legend_box: tuple of floats, eg (0.0, 0.05, 0.01, 0.7)
    :param tuple(int) fig_size: figure size
    :param int font_size: title font size
    :param str face_color: backgroud color (eg, white, black)
    :param str destination: plot destination path
    """
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    df_building.plot(column='buildings', categorical=True, legend=True,
                     ax=ax, linewidth=0.1, cmap='Dark2',
                     edgecolor="0.8")

    # ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("building")
    leg.set_bbox_to_anchor(legend_box)
    plt.axis("off")
    plt.title("Building infrastructure in Oldenburg", fontsize=font_size)
    plt.savefig(destination+"buildings.png", facecolor=fig.get_facecolor(),
                dpi=300)


def plot_landuses(df_building, df_landuse, legend_box, fig_size, font_size,
                  face_color, destination):
    """Plot polygons for landuse.

    :param DataFrame df_building: dbuilding georeferenced data (geodataframe)
    :param DataFrame df_landuse: landuse georeferenced data
    :param tuple(float) legend_box: tuple of floats, eg (0.0, 0.05, 0.01, 0.7)
    :param tuple(int) fig_size: figure size
    :param int font_size: title font size
    :param str face_color: backgroud color (eg, white, black)
    :param str destination: plot destination path
    """
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    base = df_landuse.plot(column='landuse', categorical=True,
                           legend=True, ax=ax, linewidth=0.1,
                           cmap='tab10', edgecolor="0.8")
    df_building.plot(ax=base, edgecolor="0.8", color='white', legend=True)

    # ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("landuse")
    leg.set_bbox_to_anchor(legend_box)
    plt.axis("off")
    plt.title("Land use in Oldenburg", fontsize=font_size)
    plt.savefig(destination+"landuse.png", facecolor=fig.get_facecolor(),
                dpi=300)


def plot_roads(df_highway, legend_box, fig_size, font_size, face_color,
               destination):
    """Plot lines (highway).

    :param DataFrame df_highway: highway georeferenced data (geodataframe)
    :param tuple(float) legend_box: tuple of floats, eg (0.0, 0.05, 0.01, 0.7)
    :param tuple(int) fig_size: figure size
    :param int font_size: title font size
    :param str face_color: backgroud color (eg, white, black)
    :param str destination: plot destination path
    """
    fig, ax = plt.subplots(1, figsize=fig_size, facecolor=face_color)
    df_highway.plot(column='highway', categorical=True, legend=True,
                    ax=ax, linewidth=1, cmap='tab10', edgecolor="0.8")

    # ax.set_facecolor("whitesmoke")
    leg = ax.get_legend()
    leg.set_title("highway")
    leg.set_bbox_to_anchor(legend_box)
    plt.title("Roads infrastructure in Oldenburg", fontsize=font_size)
    plt.axis("off")
    plt.savefig(destination+"highway.png", facecolor=fig.get_facecolor(),
                dpi=300)


if __name__ == "__main__":
    csv_file = "../data/02_urban_output_data/"
    buildings_shp = csv_file+"buildings/buildings.shp"
    landuse_shp = csv_file+"landuse/landuse.shp"
    highway_shp = csv_file+"highway/highway.shp"
    destination = "../data/04_Visualisation/"

    df_building = gpd.read_file(buildings_shp)
    df_highway = gpd.read_file(highway_shp)
    df_landuse = gpd.read_file(landuse_shp)
    classifications = ["commercial", "retail", "residential", "farmland",
                       "farmyard", "industrial"]
    df_landuse = df_landuse.loc[df_landuse["landuse"].isin(classifications)]

    sns.set_style("dark")
    sns.set_context(context=None, font_scale=1, rc=None)
    legend_box = (0.0, 0.05, 0.01, 0.7)
    font_size = 11
    fig_size = (6, 4)
    face_color = "white"

    plot_landuses(df_building, df_landuse, legend_box, fig_size, font_size,
                  face_color, destination)
    plot_roads(df_highway, legend_box, fig_size, font_size, face_color,
               destination)
    plot_building(df_building, legend_box, fig_size, font_size, face_color,
                  destination)

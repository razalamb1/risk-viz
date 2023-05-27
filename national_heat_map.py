"""Create a nationwide Heat Map."""


import pandas as pd
import src.heat_maps as hm
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import geopandas as gpd

# get token
load_dotenv()
token = os.environ.get("TOKEN")


def heat_map(
    gdf: gpd.GeoDataFrame,
    column: str,
    colormap: str,
    name: str,
    county: str,
    state: str,
) -> plt.figure:
    """Graph heat map given GeoDataFrame.

    Args:
        gdf: GeoDataFrame from call to merge_data() function.
        column: The name of the column in the gdf to graph.
        colormap: The matplotlib colormap to use.
        name: The name used for the title of the heat map.
        county: The county from which the data belongs to.
        state: The state from which the data belongs to.
    Returns:
        Figure object.
    """
    csfont = {"fontname": "Arial"}
    ax = gdf.plot(
        figsize=(15, 15),
        column=column,
        cmap=colormap,
        legend=True,
        legend_kwds={
            "shrink": 0.5,
            "label": "Percent of 18+ Population",
            "format": "%.0f%%",
        },
        missing_kwds={
            "color": "grey",
            "label": "Missing values",
        },
        alpha=0.8,
        edgecolor="#808080",
        linewidth=0.1,
    )
    # cx.add_basemap(ax)
    ax.set_axis_off()
    if county == "all":
        ax.set_title(f"{name} in {state}", fontsize=20, **csfont)
    else:
        ax.set_title(
            f"{name} in {county} County, {state}",
            fontsize=20,
            **csfont,
        )
    return ax


# Specifications for access_api call.
columns = [
    "BPHIGH_CrudePrev",
    "CSMOKING_CrudePrev",
    "OBESITY_CrudePrev",
    "DIABETES_CrudePrev",
    "LPA_CrudePrev",
    "SLEEP_CrudePrev",
]
names = [
    "Hypertension",
    "Current Smokers",
    "Obesity",
    "Diabetes",
    "Physical Inactivity",
    "Less than 7 Hours of Sleep",
]
cmaps = ["Purples", "Blues", "Greens", "Reds", "YlOrBr", "Oranges"]

# all states to access
states = [
    "Alabama",
    "Arkansas",
    "Arizona",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    # "Hawaii",
    "Iowa",
    "Idaho",
    "Illinois",
    "Indiana",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Massachusetts",
    "Maryland",
    "Maine",
    "Michigan",
    "Minnesota",
    "Missouri",
    "Mississippi",
    "Montana",
    "North Carolina",
    "North Dakota",
    "Nebraska",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "Nevada",
    "New York",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Virginia",
    "Vermont",
    "Washington",
    "Wisconsin",
    "West Virginia",
    "Wyoming",
]

gdf_list = []

for state in states:
    geoResults = hm.access_api(
        columns,
        state,
        tract=False,
        token=token,
    )
    gdf = hm.convert_data(geoResults)
    gdf = hm.merge_data(gdf, state, "all", False)
    gdf_list.append(gdf.to_crs(epsg=3857))


# Convert all to one list
rdf = gpd.GeoDataFrame(pd.concat(gdf_list), crs=gdf_list[0].crs)

for risk in range(len(columns)):
    rdf[columns[risk]] = rdf[columns[risk]].astype(float)
    fig = heat_map(
        rdf,
        columns[risk],
        cmaps[risk],
        names[risk],
        "all",
        "the United States",
    )
    fig.figure.savefig(
        f"images/{names[risk]}_National.png",
        bbox_inches="tight",
        dpi=400,
    )

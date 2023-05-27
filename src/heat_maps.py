"""Create heatmaps from CDC PLACES data."""
from inspect import BoundArguments
from sodapy import Socrata
import geopandas as gpd
import addfips
import contextily as cx
import matplotlib.pyplot as plt


def access_api(
    columns: list[str],
    state: str,
    county: str = "all",
    tract: bool = True,
    token: str = None,
) -> dict:
    """Fetch CDC PLACES data.

    Retrives geoJSON of PLACES data given a specific state, county, and
    conditions of interest.

    Args:
        columns: Columns to request from the dataset. Automatically includes
        state name, county name, geographical column, and FIPS code.
        state: Full state name with the first letter capitalized (i.e.
        California)
        county: County name with the first letter capitalized (i.e. Maricopa).
        Default is to return all counties.
        tract: A boolean indicator for whether or not to use tract-level data.
        token: a socrata token for accessing the API. This is not require, but
        will result in faster responses if provided.

    Returns:
        A geoJSON.

    For column names and more information, see: https://www.cdc.gov/places/
    """
    socrata_domain = "chronicdata.cdc.gov"
    socrata_dataset_identifier = "yjkw-uj5s"
    # App Tokens can be generated at https://opendata.socrata.com/signup
    # Tokens are optional (`None` can be used instead), though requests will
    # be rate limited
    client = Socrata(socrata_domain, token)
    c = columns
    selects = (
        "statedesc, countyname, geolocation, tractfips, totalpopulation, "
        + ", ".join(c)
    )
    if tract:
        if county != "all":
            results = client.get(
                socrata_dataset_identifier,
                where=f"statedesc = '{state}' and countyname = '{county}'",
                select=selects,
                content_type="geoJSON",
                limit=3000,
            )
            return results
        else:
            results = client.get(
                socrata_dataset_identifier,
                where=(f"statedesc = '{state}'"),
                select=selects,
                content_type="geoJSON",
                limit=10000,
            )
            return results
    else:
        selects = (
            "statedesc, countyname, geolocation, totalpopulation, countyfips, "
            + ", ".join(c)
        )
        socrata_dataset_identifier = "i46a-9kgh"
        results = client.get(
            socrata_dataset_identifier,
            where=(f"statedesc = '{state}'"),
            select=selects,
            content_type="geoJSON",
            limit=10000,
        )
        return results


def convert_data(geoJSON: dict) -> gpd.GeoDataFrame:
    """Convert geoJSON to geopandas DataFrame.

    Args:
        geoJSON: geoJSON from a call to the access_api() function.
    Returns:
        GeoDataFrame.
    """
    return gpd.GeoDataFrame.from_features(geoJSON["features"])


def merge_data(
    data: gpd.GeoDataFrame,
    state: str,
    county: str = "all",
    tract: bool = True,
) -> gpd.GeoDataFrame:
    """Merge Census tract data with data from API call.

    Args:
        data: GeoDataFrame from call to convert_data() function.
        state: The state from which the data belongs to.
        county: The county from which the data belongs to, defaults to all
        counties within the state.
        tract: A boolean indicator for whether or not to use tract-level data.
    Returns:
        GeoDataFrame.
    """
    if tract:
        af = addfips.AddFIPS()
        fips = af.get_state_fips(state)
        boundaries = gpd.read_file(f"data/{fips}.geojson")
        if county == "all":
            temp = boundaries.merge(
                data,
                how="left",
                left_on="GEOID",
                right_on="tractfips",
            )
        else:
            county_fips = af.get_county_fips(county, state=state)[2:]
            boundaries = boundaries[boundaries["COUNTYFP"] == county_fips]
            temp = boundaries.merge(
                data,
                how="left",
                left_on="GEOID",
                right_on="tractfips",
            )
        output = gpd.GeoDataFrame(temp, geometry="geometry_x")
        return output
    else:
        boundaries = gpd.read_file("data/cb_2018_us_county_20m")
        boundaries["totalfips"] = boundaries["STATEFP"] + boundaries["COUNTYFP"]
        temp = boundaries.merge(
            data, how="right", left_on="totalfips", right_on="countyfips"
        )
        output = gpd.GeoDataFrame(temp, geometry="geometry_x")
        return output


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
        linewidth=0.6,
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


def full_process(
    columns: list[str],
    names: list[str],
    state: str,
    county: str = "all",
    cmaps=None,
    token: str = None,
    tract: bool = True,
) -> None:
    """Extract, process, and graph CDC PLACES data.

    Accesses data from Socrata CDC PLACES API, merges with appropraite Census
    data, and graphs a heat map for each provided column.

    Args:
        columns: List of columns to request from the dataset. Automatically
        includes state name, county name, geographical column, and FIPS code.
        names: List of names to use as titles for heat maps. Should be in the
        same order as the list of columns.
        state: Full state name with the first letter capitalized (i.e.
        California)
        county: County name with the first letter capitalized (i.e. Maricopa).
        Default is to return all counties.
        cmaps: List of color maps to use to generate heat maps. Should be in
        the same order as the list of columns. Default is to use YlOrBr.
        token: Socrata API token. Default is no token, which will be slower.

    Returns:
        Nothing. Image file is saved in image folder under format
        {state}_{county}_{name}.img.
    """
    data = access_api(columns, state, county, tract, token)
    gdf = convert_data(data)
    merged_gdf = merge_data(gdf, state, county, tract)
    merged_gdf = merged_gdf.to_crs(epsg=3857)
    for risk in range(len(columns)):
        merged_gdf[columns[risk]] = merged_gdf[columns[risk]].astype(float)
        if cmaps is None:
            fig = heat_map(
                merged_gdf, columns[risk], "YlOrBr", names[risk], county, state
            )
        else:
            fig = heat_map(
                merged_gdf,
                columns[risk],
                cmaps[risk],
                names[risk],
                county,
                state,
            )
        fig.figure.savefig(
            f"images/{state}_{county}_{names[risk]}.png",
            bbox_inches="tight",
            dpi=250,
        )
    pass

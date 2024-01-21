import pandas as pd
import plotly.express as px
import geopandas as gpd

country = pd.read_csv("static/data/country.csv")
states = pd.read_csv("static/data/states.csv")
states = states[~states["Actual(mm)"].str.contains("-")]
states = states[~states["Normal(mm)"].str.contains("-")]
states = states[~states["Deviation(%) from normal"].str.contains("-")]
states["Actual(mm)"] = states["Actual(mm)"].astype(float)
states["Normal(mm)"] = states["Normal(mm)"].astype(float)
states["Deviation(%) from normal"] = states["Deviation(%) from normal"].astype(float)

rainfall_flood = gpd.read_file(
    "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
)
rainfall_flood = rainfall_flood[["ST_NM"]]
rainfall_flood["value"] = 0
rainfall_flood.loc[rainfall_flood["ST_NM"] == "Maharashtra", "value"] = 1
rainfall_flood.loc[rainfall_flood["ST_NM"] == "Bihar", "value"] = 1
rainfall_flood.loc[rainfall_flood["ST_NM"] == "Himachal Pradesh", "value"] = 1


def hist():
    fig = px.histogram(states, x="Actual(mm)")
    return fig


def bar():
    fig = px.bar(states, x="STATE", y="Actual(mm)")
    return fig


def line():
    fig = px.line(country.head(36), x="Dates", y="ACTUAL (mm)")
    return fig


def line_5y():
    fig = px.line(country.head(60), x="Dates", y="ACTUAL (mm)")
    return fig


def line_10y():
    fig = px.line(country.head(120), x="Dates", y="ACTUAL (mm)")
    return fig


def index_map():
    fig = px.choropleth(
        rainfall_flood,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="ST_NM",
        color="value",
        color_continuous_scale="Blues",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    # disable heatbar
    fig.update_layout(coloraxis_showscale=False)
    # make padding zero
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def density(subset, center, zoom):
    fig = px.density_mapbox(
        subset,
        lat="Latitude",
        lon="Longitude",
        z="Area Affected",
        radius=10,
        center=center,
        zoom=zoom,
        mapbox_style="stamen-terrain",
    )
    return fig


def choloropeth1(subset, geojson):
    fig = px.choropleth(
        subset,
        geojson=geojson,
        featureidkey="properties.ST_NM",
        locations="loc",
        color="Severity",
        color_continuous_scale="Blues",
    )

    fig.update_geos(fitbounds="locations", visible=False)
    return fig


def choloropeth2(subset):
    fig = px.choropleth(
        subset,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey="properties.ST_NM",
        locations="loc",
        color="Area Affected",
        color_continuous_scale="Reds",
    )

    fig.update_geos(fitbounds="locations", visible=False)
    return fig


def choloropeth3(subset, geojson):
    fig = px.choropleth(
        subset,
        geojson=geojson,
        featureidkey="properties.ST_NM",
        locations="loc",
        color="Human fatality",
        color_continuous_scale="Reds",
    )

    fig.update_geos(fitbounds="locations", visible=False)
    return fig

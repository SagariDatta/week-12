"""
app2.py: use "template2.html" to allow the user to specify the number 
of days to query
"""
from flask import render_template, request
from flask import Flask
import requests
import geopandas as gpd
import altair as alt
import numpy as np

# initialize the app
app = Flask(__name__)

# load the neighborhoods
hoods = gpd.read_file(
    "https://raw.githubusercontent.com/MUSA-620-Spring-2019/week-12/master/data/zillow_neighborhoods.geojson"
)


def get_data(days):
    """
    Query the CARTO database to get shootings from the recent past.
    
    Parameters
    ----------
    days : int
        the number of days to get data for
    
    Returns
    -------
    gdf : GeoDataFrame
        the data frame holding the queried data
    """
    query = "SELECT * FROM shootings WHERE date_ >= current_date - %d" % (days)
    r = requests.get(
        "https://phl.carto.com/api/v2/sql", params={"q": query, "format": "geojson"}
    )
    gdf = gpd.GeoDataFrame.from_features(r.json(), crs={"init": "epsg:4326"})
    gdf = gdf.dropna()

    gdf["fatal"] = gdf["fatal"].map({0: "No", 1: "Yes"})

    return gdf


def make_chart(data, days):
    """
    Make an Altair chart
    """
    columns = ["ZillowName", "fatal"]
    data = data[columns]

    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            y=alt.Y(
                "ZillowName:N",
                title="Neighborhood",
                sort=alt.EncodingSortField(
                    op="count",  # The operation to run on the field prior to sorting
                    order="descending",  # The order to sort in
                ),
            ),
            x=alt.X("count()", title="Number of Shootings"),
            color=alt.Color("fatal:N", title="Fatal?"),
            tooltip=[
                alt.Tooltip("count()", title="Number of Shootings"),
                alt.Tooltip("ZillowName", title="Neighborhood"),
                alt.Tooltip("fatal", title="Fatal?"),
            ],
        )
        .properties(
            width=400,
            height=800,
            title="Shootings in the Last %d Days by Neighborhood" % days,
        )
    )


@app.route("/chart")
def chart(days=365):
    """
    Get the altair chart JSON specification.
    """
    # the days parameter (optional)
    days = request.args.get("days", default=365, type=int)

    # query the CARTO database
    gdf = get_data(days)

    # do a spatial join with ZIP codes
    hoods.crs = gdf.crs
    joined = gpd.sjoin(gdf, hoods, how="left", op="within").dropna(
        subset=["ZillowName"]
    )

    # make our chart
    chart = make_chart(joined, days)

    # return the JSON specification
    return chart.to_json()


@app.route("/")
def index():
    """
    The default index of the page.
    """
    return render_template("template2.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


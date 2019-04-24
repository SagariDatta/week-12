from flask import render_template, request
from flask import Flask
import requests
import geopandas as gpd

app = Flask(__name__)


@app.route("/shootings/")
def hello(days=90, fatal=0):
    """
    Two optional request parameters:

    days: the number of days to query shootings for
    fatal: 0/1 indicating nonfatal vs fatal
    """

    # get the optional request args
    days = request.args.get("days", default=90, type=int)
    fatal = request.args.get("fatal", default=0, type=int)

    # create our SQL query
    query = (
        "SELECT * FROM shootings WHERE date_ >= current_date - %d AND fatal = %d"
        % (days, fatal)
    )

    # query the CARTO database
    r = requests.get(
        "https://phl.carto.com/api/v2/sql", params={"q": query, "format": "geojson"}
    )

    # count the number of fatal/non-fatal shootings
    gdf = gpd.GeoDataFrame.from_features(r.json())
    count = (gdf["fatal"] == fatal).sum()

    # return the count
    if fatal == 1:
        return "There have been %d fatal shootings in the past %d days" % (count, days)
    else:
        return "There have been %d nonfatal shootings in the past %d days" % (
            count,
            days,
        )


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


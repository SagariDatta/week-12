import dash
import dash_core_components as dcc
import dash_html_components as html
import altair as alt
import io
from vega_datasets import data

# load the data
cars = data.cars()

# initialize the app
app = dash.Dash(__name__)

# add external styling
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# set a title
app.title = "Testing Dash and Altair"

# columns to plot
COLUMNS = [
    "Miles_per_Gallon",
    "Acceleration",
    "Displacement",
    "Cylinders",
    "Weight_in_lbs",
]

# set the layout
app.layout = html.Div(
    [
        html.Div(
            [
                # Dropdown for x axis
                html.Div(
                    [
                        html.Label("x-axis"),
                        dcc.Dropdown(
                            id="x_axis",
                            options=[{"label": i, "value": i} for i in COLUMNS],
                            value="Acceleration",
                        ),
                    ],
                    style={
                        "width": "250px",
                        "margin-right": "auto",
                        "margin-left": "auto",
                        "text-align": "center",
                    },
                ),
                # Dropdown for y axis
                html.Div(
                    [
                        html.Label("y-axis"),
                        dcc.Dropdown(
                            id="y_axis",
                            options=[{"label": i, "value": i} for i in COLUMNS],
                            value="Miles_per_Gallon",
                        ),
                    ],
                    style={
                        "width": "250px",
                        "margin-right": "auto",
                        "margin-left": "auto",
                        "text-align": "center",
                    },
                ),
            ],
            style={"display": "flex", "justify-content": "center"},
        ),
        # this is where the chart goes
        html.Iframe(
            id="plot",
            height="500",
            width="1000",
            sandbox="allow-scripts",
            style={"border-width": "0px"},
        ),
    ]
)


@app.callback(
    dash.dependencies.Output("plot", "srcDoc"),
    [
        dash.dependencies.Input("x_axis", "value"),
        dash.dependencies.Input("y_axis", "value"),
    ],
)
def make_figure(x_axis, y_axis):

    brush = alt.selection_interval()
    base = alt.Chart(cars)

    # scatter plot of x vs y
    scatter = (
        base.mark_point()
        .encode(x=x_axis, y=y_axis, color="Origin:N")
        .properties(width=250, height=400, selection=brush)
    )

    # histogram of horsepower
    hist = (
        base.mark_bar()
        .encode(x=alt.X("Horsepower:Q", bin=True), y="count()", color="Origin:N")
        .transform_filter(brush.ref())
    ).properties(height=375)

    chart = alt.hconcat(scatter, hist)

    # Save html as a StringIO object in memory
    cars_html = io.StringIO()
    chart.save(cars_html, "html")

    # Return the html from StringIO object
    return cars_html.getvalue()


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5000, debug=True)

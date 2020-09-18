import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import countries_df, totals_df
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(
    # * plotly.express scatter_geo를 사용, API 참조
    countries_df,
    title="Confirmed Cases by Countries",
    hover_name="Country_Region",
    hover_data={
        "Confirmed": ":,2f",
        "Recovered": ":,2f",
        "Deaths": ":,2f",
        "Country_Region": False
    },
    color="Confirmed",
    locations="Country_Region",
    locationmode="country names",
    projection="natural earth",
    color_continuous_scale=px.colors.sequential.Oryel,
    size="Confirmed",
    size_max=40,
    template="plotly_dark"
)

bubble_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)
)

bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    color=["Confirmed", "Deaths", "Recovered"],
    template="plotly_dark",
    title="Total Global Cases",
    hover_data={'count': ":,"},
    labels={
      "condition": "Condition",
      "count": "Count",
      "color": "Condition"
    }
)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    # html.element로 태그를 생성하고 style={}로 css 설정 가능
    # ! react를 이용하기 때문에 style은 object notation으로 써야함
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            style={"display": "grid", "gap": 50,
                   "gridTemplateColumns": "repeat(4, 1fr)"},
            children=[
                html.Div(style={"grid-column": "span 3"},
                         children=[dcc.Graph(figure=bubble_map)]),
                html.Div(children=[make_table(countries_df)]),
            ]
        ),
        html.Div(
            style={"display": "grid", "gap": 50,
                   "gridTemplateColumns": "repeat(4, 1fr)"},
            children=[html.Div(children=[dcc.Graph(figure=bars_graph)])])
    ],
)

map_figure = px.scatter_geo(countries_df)
map_figure.show()


if __name__ == "__main__":
    app.run_server(debug=True)

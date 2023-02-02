import dash
import pandas as pd
import pathlib
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
from helpers import compute_data_choice_1, compute_data_choice_2, airline_data
import base64

external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=external_stylesheets,
    title="US Domestic Airline Flights Performance"
)

server = app.server


REPORT_TYPE = ['Yearly Airline Performace Report',
               'Yearly Airline Delay Report']

YEAR_RANGE = [*range(2005, 2021)]

BRIEFINGS = ["""For the chosen year provide,
-   Number of flights under different cancellation categories using bar chart.
-   Average flight time by reporting airline using line chart.
-   Percentage of diverted airport landings per reporting airline using pie chart.
-   Number of flights flying from each state using `choropleth` map.
-   Number of flights flying to each state from each reporting airline using treemap chart.
             """, """For the chosen year provide,
-   Monthly average carrier delay by reporting airline for the given year.
-   Monthly average weather delay by reporting airline for the given year.
-   Monthly average national air system delay by reporting airline for the given year.
-   Monthly average security delay by reporting airline for the given year.
-   Monthly average late aircraft delay by reporting airline for the given year.
             """]


"""
<a href="https://github.com/icheft/US-Domestic-Airline-Flights-Performance" class="github-corner" aria-label="View source on GitHub"></a>
"""
encoded = base64.b64encode(open("static/github.svg", 'rb').read())
githubSvg = 'data:image/svg+xml;base64,{}'.format(encoded.decode())

app.layout = html.Div(
    [
        html.A([
            html.Img(
                src=githubSvg,
                style={
                    'float': 'right',
                    'position': 'relative',
                    'padding-top': 0,
                    'padding-right': 0
                },
                className='github-corner'
            )
        ], href='https://github.com/icheft/US-Domestic-Airline-Flights-Performance', title='View source on GitHub', **{'aria-label': 'View source on GitHub'}),

        html.Div(
            [html.Img(src=app.get_asset_url("IBM-Logo.png"))], className="app__banner"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "US Domestic Airline Flights Performance",
                                    className="title",
                                    style={'color': '#503D36', }
                                ),
                                dcc.Markdown(
                                    """**[Data Visualization with Python](https://www.coursera.org/learn/python-for-data-visualization) Final Project**   
                                    Demonstrating the data visualization skills learned in the course.  
                                    Dashboard is based on the concept of demonstrating US Domestic Airline Flights Performance for a given year (2005 to 2020)."""
                                ),
                            ]
                        )
                    ],
                    className="app__header",
                ),
                html.Div(
                    [
                        html.Div(
                            children=[
                                html.Div(
                                    [html.Div(
                                        [
                                            html.Label(
                                                ["Report Type: ", dcc.Dropdown(
                                                    id="input-type",
                                                    multi=False,
                                                    placeholder="Select a report type",
                                                    value=REPORT_TYPE[0],
                                                    options=[{"label": i, "value": i}
                                                             for i in REPORT_TYPE],
                                                )]
                                            ),
                                        ],
                                        className="app__dropdown",
                                    ),
                                        html.Div(
                                        [
                                            html.Label(
                                                ["Choose Year: ", dcc.Dropdown(
                                                    id="input-year",
                                                    multi=False,
                                                    value=YEAR_RANGE[0],
                                                    placeholder="Select a year to inspect",
                                                    options=[{"label": i, "value": i}
                                                             for i in YEAR_RANGE],
                                                )]
                                            ),
                                        ],
                                        className="app__dropdown",
                                    ), ],
                                    className="col"
                                ),
                                html.Div(
                                    [dcc.Markdown(
                                        id='intro',
                                    ), ],
                                    className="col m-r-5"
                                )
                            ],
                            className='row justify-content-center'
                        ), ],
                    className="container card app__content",
                ),
                html.Br(),

                html.Div(
                    [
                        html.Div([], id='plot1'),

                        html.Div([
                            html.Div([], id='plot2', className='col'),
                            html.Div([], id='plot3', className='col')
                        ], className='row'),

                        html.Div([
                            html.Div([], id='plot4', className='col'),
                            html.Div([], id='plot5', className='col')
                        ], className='row'),
                    ],
                    className="container card app__content bg-white",
                ),
            ],
            className="app__container",
        ),
        html.Footer(
            className="my-5 pt-5 text-muted text-center text-small",
            children=[
                html.Span(children="Copyright (C) 2021 by "),
                html.A(href="https://github.com/icheft",
                       children="Brian L. Chen")
            ]
        )
    ]
)


@app.callback(
    Output('intro', 'children'),
    [Input('input-type', 'value')]
)
def render_intro(report_type):
    for i, intro in enumerate(BRIEFINGS):
        if report_type == REPORT_TYPE[i]:
            return intro
    return "Please choose a report type to begin."

# Start task


@app.callback([Output('plot1', 'children'),
               Output('plot2', 'children'),
               Output('plot3', 'children'),
               Output('plot4', 'children'),
               Output('plot5', 'children')],
              [Input(component_id='input-type', component_property='value'),
               Input(component_id='input-year', component_property='value')],
              [State("plot1", 'children'), State("plot2", "children"),
               State("plot3", "children"), State("plot4", "children"),
               State("plot5", "children")
               ])
# Add computation to callback function and return graph
def get_graph(chart, year, children1, children2, c3, c4, c5):

    # Select data
    df = airline_data[airline_data['Year'] == int(year)]

    if chart == REPORT_TYPE[0]:
        # Compute required information for creating graph from the data
        bar_data, line_data, div_data, map_data, tree_data = compute_data_choice_1(
            df)

        # Number of flights under different cancellation categories
        bar_fig = px.bar(bar_data, x='Month', y='Flights',
                         color='CancellationCode', title='Monthly Flight Cancellation')

        line_fig = px.line(line_data, x='Month', y='AirTime', color='Reporting_Airline',
                           title='Average monthly flight time (minutes) by airline')

        # Percentage of diverted airport landings per reporting airline
        pie_fig = px.pie(div_data, values='Flights', names='Reporting_Airline',
                         title='% of flights by reporting airline')

        map_fig = px.choropleth(map_data,  # Input data
                                locations='OriginState',
                                color='Flights',
                                hover_data=['OriginState', 'Flights'],
                                locationmode='USA-states',  # Set to plot as US States
                                color_continuous_scale='GnBu',
                                range_color=[0, map_data['Flights'].max()])
        map_fig.update_layout(
            title_text='Number of flights from origin state',
            geo_scope='usa')  # Plot only the USA instead of globe

        tree_fig = px.treemap(tree_data, path=['DestState', 'Reporting_Airline'],
                              values='Flights',
                              color='Flights',
                              color_continuous_scale='RdBu',
                              title='Flight count by airline to destination state'
                              )

        return [dcc.Graph(figure=tree_fig),
                dcc.Graph(figure=pie_fig),
                dcc.Graph(figure=map_fig),
                dcc.Graph(figure=bar_fig),
                dcc.Graph(figure=line_fig)
                ]
    else:
        # Compute required information for creating graph from the data
        avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_data_choice_2(
            df)

        # Create graph
        carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
                              title='Average carrrier delay time (minutes) by airline')
        weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                              title='Average weather delay time (minutes) by airline')
        nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
                          title='Average NAS delay time (minutes) by airline')
        sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
                          title='Average security delay time (minutes) by airline')
        late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                           title='Average late aircraft delay time (minutes) by airline')

        return[dcc.Graph(figure=carrier_fig),
               dcc.Graph(figure=weather_fig),
               dcc.Graph(figure=nas_fig),
               dcc.Graph(figure=sec_fig),
               dcc.Graph(figure=late_fig)]


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

def create_dash_app(df):
    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(id='scatter-plot', config={'displayModeBar': False}),
        html.Div(id='click-data')
    ])

    @app.callback(
        Output('scatter-plot', 'figure'),
        Input('scatter-plot', 'clickData')
    )
    def update_figure(click_data):
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
        return fig

    @app.callback(
        Output('click-data', 'children'),
        Input('scatter-plot', 'clickData')
    )
    def display_click_data(click_data):
        if click_data:
            point_index = click_data['points'][0]['pointIndex']
            return f"Clicked on point: {df.iloc[point_index].to_dict()}"
        return "Click on a point in the scatter plot."

    return app

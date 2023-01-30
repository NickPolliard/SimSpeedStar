import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas
import requests
import logging

from app import dapp
from apps.elements.stake_navbar import navbar, banner
from apps.elements.plan import Grid, generate_dropdown_form, generate_input_form

from .data import locations_check, etl_check, metrics

#region Pandas options
pandas.options.display.float_format = '{:,.10f}'.format
pandas.set_option("display.max_columns", 20)
pandas.set_option('expand_frame_repr', False)
#endregion


#region FOR GMV BarGraph
# def get_GMV_data():
try:
    GMV_json = requests.get('http://bq-data-api.default.svc.cluster.local/GMV')
    # GMV_json.raise_for_status()
    df = pandas.DataFrame(GMV_json.json()['data'])
except Exception as e:
    logging.error('Could not connect to BQ API')
    GMV_json = [{"count": 0, "data": [], "page": 1, "size": 100}]
    df = pandas.DataFrame(GMV_json[0]['data'])
if df.empty:
    df['TransactionMonth'] = 0
    df['GMVTotal'] = 0
fig = px.bar(df, x="TransactionMonth", y='GMVTotal', title="GMV By Month")

#endregion



#region Page Grid Definition -- Change rows and column sizes here
page_grid = Grid(rows=4,cols=3, specs=[[{'width': 12}, None, None], [{'width': 12}, None, None], [{'width': 0}, {'width': 12}, None], [{}, None, None]],
                 row_kwargs=[{'className': 'p-2'}, {'className': 'p-2'}, {'className': 'pt-5', 'align': 'center'}, {'className': 'p-2'}],
                 div_class_name='page-grid')
#endregion



#region Nav Roq and page_grid elements
nav_row = Grid(1, 1)
nav_row.add_element(html.Div([
    navbar('setup'),
], className='d-flex flex-row justify-content-between align-items-center'), 1, 1)
page_grid.add_element(nav_row.generated_grid, 1, 1)
page_grid.add_element(html.Div([dcc.Graph(figure=fig)], className='d-flex flex-row justify-content-between align-items-center'), 3, 2)
#endregion



#region General Layout
layout = html.Div([
    banner(),
    page_grid.generated_grid,
    dcc.Interval(
        id='interval-component',
        interval=600*1000, # in milliseconds
        n_intervals=0
    )
])
#endregion
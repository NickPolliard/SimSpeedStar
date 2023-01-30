import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from datetime import datetime, timedelta
import pandas

from app import dapp
from apps.elements.navbar import navbar, banner
from apps.elements.plan import Grid, generate_dropdown_form, generate_input_form

from .data import locations_check, etl_check, metrics

#region Pandas options
pandas.options.display.float_format = '{:,.10f}'.format
pandas.set_option("display.max_columns", 20)
pandas.set_option('expand_frame_repr', False)
#endregion


#region Dropdown Stuff
collection_enum = [{'label': 'Sales', 'value': 'Sales'},
                   {'label': 'Payments', 'value': 'Payments'},
                   {'label': 'ItemsInCart', 'value': 'ItemsInCart'},
                   {'label': 'Discounts', 'value': 'Discounts'}]

dataset_enum = [{'label': 'Customer View', 'value': 'Customer View'},
                {'label': 'Backup', 'value': 'Backup'},
                {'label': 'Weekly', 'value': 'Weekly'}]

collection_selection = Grid(1, 3)
collection_selection.add_element(html.H1('Choose a collection to analyze'), 1, 1)

collection_dropdown = generate_dropdown_form(label_kwargs={'children': 'Collection Selection'},
                                             dropdown_kwargs={'id': 'collections', 'options': collection_enum})

collection_selection.add_element(collection_dropdown, 1, 2)


dataset_dropdown = generate_dropdown_form(label_kwargs={'children': 'DataSet Selection'},
                                          dropdown_kwargs={'id': 'dataset', 'options': dataset_enum})
collection_selection.add_element(dataset_dropdown, 1, 3)
#endregion

# region DataTable for Location Detail View
location_detail_div = html.Div(children=[], className='d-flex flex-row justify-content-between align-items-center', id='locationsDetail')

@dapp.callback(
  [Output('locationsDetail', 'children')],
    [Input('collections', 'value'), Input("dataset", "value")]
)
def create_location_detail_table(collection, dataset):
    if dataset == 'Weekly':
        max_date = datetime.today() - timedelta(days=7)
    elif dataset == 'backup':
        max_date = datetime.today() - timedelta(days=3)
    else:
        max_date = datetime.today() - timedelta(days=2)
    max_date = max_date.strftime("%Y-%m-%d")
    if not collection:
        collection = 'Sales'
    return [dcc.Loading(dbc.Table.from_dataframe(metrics.get_location_detail_view(collection, dataset, max_date), striped=True, bordered=True, hover=True))]

# endregion



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
page_grid.add_element(collection_selection.generated_grid, 2, 1)
page_grid.add_element(location_detail_div, 3, 2)
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
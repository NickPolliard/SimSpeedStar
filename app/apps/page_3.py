import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

import pandas

from app import dapp
from apps.elements.navbar import navbar, banner
# from apps.elements.plan import Grid, generate_dropdown_form, generate_input_form
from apps.elements.plan import Grid
from apps.elements import status_components as status


pandas.options.display.float_format = '{:,.10f}'.format
pandas.set_option("display.max_columns", 20)
pandas.set_option('expand_frame_repr', False)


##################
# Dashboard Layout
##################
# Page Grid object generation
page_grid = Grid(rows=4,cols=4, specs=[[{'width': 10}, {'width': 2}, None, None], [{'width': 12}, None, None, None], 
                                       [{'width': 0}, {'width': 12}, {'width': 0}, {'width': 0}], [{}, None, None, None]], 
                 row_kwargs=[{'className': 'p-2'}, {'className': 'p-2'}, {'className': 'pt-5', 'align': 'center'}, {'className': 'p-2'}], 
                 div_class_name='page-grid')

# region Row for nav and continue button
nav_row = html.Div([
    navbar('status')
], className='d-flex flex-row justify-content-between align-items-center')
# endregion


page_grid.add_element(nav_row, 1, 1)


# We generate the layout with the grid
layout = html.Div([
    banner(),
    page_grid.generated_grid,
    dcc.Interval(
        id='interval-component',
        interval=600*1000,  # in milliseconds
        n_intervals=0
    )
], id='main-layout')


@dapp.callback(Output("main-layout", "children"), [Input("interval-component", "n_intervals")])
def update(n_intervals):
    print('refreshed')
#    status_grid = status.generate_status()
#    page_grid.replace_element(status_grid.generated_grid, 2, 1)
    return [
        banner(),
        page_grid.generated_grid,
        dcc.Interval(
            id='interval-component',
            interval=600*1000,  # in milliseconds
            n_intervals=0
        )
    ]


################################
# Interaction Between Components
################################

#import dash
#import dash_daq as daq
#import dash_core_components as dcc
#import dash_html_components as html
#import dash_bootstrap_components as dbc
#
#from dash.dependencies import Input, Output, State
#from dash.exceptions import PreventUpdate
#
#import pandas
#
#from app import dapp
#from apps.elements.navbar import navbar, banner
#from apps.elements.plan import Grid, generate_dropdown_form, generate_input_form
#
#
##region Pandas options
#pandas.options.display.float_format = '{:,.10f}'.format
#pandas.set_option("display.max_columns", 20)
#pandas.set_option('expand_frame_repr', False)
##endregion
#
#
##region Dropdown Stuff
#collection_enum = [{'label': 'Sales', 'value': 'sales'},
#                   {'label': 'Payments', 'value': 'payments'},
#                   {'label': 'ItemsInCart', 'value': 'itemsInCart'},
#                   {'label': 'Discounts', 'value': 'discounts'}]
#dataset_enum = [{'label': 'Customer View', 'value': 'Customer View'},
#                {'label': 'Backup', 'value': 'Backup'},
#                {'label': 'Weekly', 'value': 'Weekly'}]
#
#location_df = locations_check.get_dropdown_locations()
#location_dict = location_df.to_dict(orient='records')
#location_options = [{'label': row['DisplayName'], 'value': row['_id']} for row in location_dict]
#
#collection_selection = Grid(4, 1)
#collection_selection.add_element(html.H1('Choose a collection to analyze'), 1, 1)
#
#collection_dropdown = generate_dropdown_form(label_kwargs={'children': 'Collection Selection'},
#                                             dropdown_kwargs={'id': 'collections', 'options': collection_enum})
#collection_selection.add_element(collection_dropdown, 2, 1)
#location_dropdown = generate_dropdown_form(label_kwargs={'children': 'Location Selection'},
#                                           dropdown_kwargs={'id': 'locations', 'options': location_options})
#collection_selection.add_element(location_dropdown, 3, 1)
#
#dataset_dropdown = generate_dropdown_form(label_kwargs={'children': 'DataSet Selection'},
#                                             dropdown_kwargs={'id': 'dataset', 'options': dataset_enum})
#collection_selection.add_element(dataset_dropdown, 4, 1)
##endregion
#
#
##region Row Counts Display
#row_grid = Grid(2, 2)
#mongo_card_body = dbc.CardBody(
#    [
#        html.P("0", className="card-text"),
#    ]
#)
#mongo_card_body.id = 'mongo-card-body'
#mongo_card = dbc.Card(
#    [
#        dbc.CardHeader("Mongo Row Count"),
#        mongo_card_body
#    ],
#    style={"width": "18rem"},
#)
#
#bq_card_body = dbc.CardBody(
#    [
#        html.P("0", className="card-text"),
#    ]
#)
#bq_card_body.id = 'bq-card-body'
#bq_card = dbc.Card(
#    [
#        dbc.CardHeader("Bigquery Row Count"),
#        bq_card_body
#    ],
#    style={"width": "18rem"},
#)
#bq_card.id = 'bq-card'
#mongo_card.id = 'mongo-card'
#
#
#total_sales_body = dbc.CardBody(
#    [
#        html.P("0", className="card-text"),
#    ]
#)
#total_sales_body.id = 'total_sales_body'
#ts_card = dbc.Card(
#    [
#        dbc.CardHeader("Year To Date Sales"),
#        total_sales_body
#    ],
#    style={"width": "18rem"},
#)
#ts_card.id = 'ts_card'
#
#row_grid.add_element(mongo_card, 1, 1)
#row_grid.add_element(bq_card, 1 ,2)
#row_grid.add_element(ts_card, 2 ,1)
#row_grid.id = 'row-count-group'
#
##endregion
#
#
##region Total Sales Display
## TS_row_grid = Grid(1, 2)
## total_sales_body = dbc.CardBody(
##     [
##         html.P("0", className="card-text"),
##     ]
## )
## total_sales_body.id = 'total_sales_body'
## ts_card = dbc.Card(
##     [
##         dbc.CardHeader("Total Sales"),
##         total_sales_body
##     ],
##     style={"width": "18rem"},
## )
#
## bq_card_body = dbc.CardBody(
##     [
##         html.P("0", className="card-text"),
##     ]
## )
## bq_card_body.id = 'bq-card-body'
## bq_card = dbc.Card(
##     [
##         dbc.CardHeader("Bigquery Row Count"),
##         bq_card_body
##     ],
##     style={"width": "18rem"},
## )
## bq_card.id = 'bq-card'
## ts_card.id = 'ts_card'
#
## TS_row_grid.add_element(ts_card, 1, 1)
## # TS_row_grid.add_element(bq_card, 1 ,2)
## TS_row_grid.id = 'total-sales-group'
#
##endregion
#
#
##region Get Collection Counts
#@dapp.callback(
#    [Output('bq-card-body', 'children'), Output('mongo-card-body', 'children')],
#    [Input('collections', 'value'), Input('locations', 'value'), Input("dataset", "value")]
#)
#def populate_row_counts(collection, locationId, dataset):
#    bq_count = metrics.get_bq_count(collection, locationId, dataset)
#    mongo_count = metrics.get_mongo_count(collection, locationId)
#
#    return bq_count, mongo_count
#
##endregion
#
##region Get totalSales
#@dapp.callback(
#    [Output('total_sales_body', 'children')],
#    [Input('locations', 'value')]
#)
#def populate_total_sales(locationId):
#    total_sales = metrics.get_total_sales(locationId)
#    if total_sales.empty:
#        return [0]
#    return [total_sales['CartTotal'][0]]
#
##endregion
#
##region Button Mechanics for table selector
#
#
##endregion
#
#
##region Page Grid Definition -- Change rows and column sizes here
#page_grid = Grid(rows=4,cols=2, specs=[[{}, None], [{'width': 4}, {'width': 8}], [{'width': 4}, {'width': 8}], [{}, None]],
#                 row_kwargs=[{'className': 'p-2'}, {'className': 'p-2'}, {'className': 'pt-1', 'align': 'center'}, {'className': 'p-2'}],
#                 div_class_name='page-grid')
##endregion
#
#
##region Nav Roq and page_grid elements
#nav_row = Grid(1, 1)
#nav_row.add_element(html.Div([
#    navbar('setup'),
#], className='d-flex flex-row justify-content-between align-items-center'), 1, 1)
#
#
#
#page_grid.add_element(nav_row.generated_grid, 1, 1)
#page_grid.add_element(dbc.Card(collection_selection.generated_grid, style={'min-height': '18.5 rem'}), 2, 1)
#page_grid.add_element(dbc.Card(row_grid.generated_grid, style={'min-height': '23 rem'}), 2, 2)
## page_grid.add_element(dbc.Card(TS_row_grid.generated_grid, style={'min-height': '23 rem'}), 3, 2)
##endregion
#
#
#
##region General Layout
#layout = html.Div([
#    banner(),
#    page_grid.generated_grid,
#    dcc.Interval(
#        id='interval-component',
#        interval=600*1000, # in milliseconds
#        n_intervals=0
#    )
#    ])
##endregion
#
#
#
#
#
#
#

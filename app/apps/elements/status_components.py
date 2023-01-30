from apps.data import locations_check, etl_check, metrics
from apps.elements.plan import Grid

import dash_bootstrap_components as dbc
import dash_html_components as html

from datetime import datetime, timedelta
import pandas

def generate_status():
    sales_locations_counts = etl_check.check_sales_table_counts()
    items_locations_counts = etl_check.check_items_counts()
    Discounts_locations_counts = etl_check.check_discounts_counts()
    Customers_locations_counts =  etl_check.check_customers_count()
    InventoryActivities_locations_counts = etl_check.check_inventory_activities_count()
    payments_locations_counts = etl_check.check_payments_counts()
    client_counts = locations_check.check_clients()
    location_counts = etl_check.check_locations_counts()

    status_grid = Grid(2, 4,specs=[[{'width': 3}, {'width': 3}, {'width': 3}, {'width': 3}], [{'width': 3}, {'width': 3}, {'width': 3}, {'width': 3}]],
                       row_kwargs=[{'className': 'pt-3', 'align': 'center'}, {'className': 'pt-3', 'align': 'center'}], div_class_name='page-grid')

    # region LED Indicators for Sales Counts
    if sales_locations_counts['mongo'] == sales_locations_counts['bq']:
        bg_color = 'success'
    else:
        bg_color = 'danger'
    sales_missing = sales_locations_counts['mongo'] - sales_locations_counts['bq']
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("Sales Status", className="card-text", id='saleStatus')),
            dbc.CardImg(src="", bottom=True),
            dbc.Tooltip(
                f'mongo count: {sales_locations_counts["mongo"]}, bigquery count: {sales_locations_counts["bq"]} missing: {sales_missing}',
                target="saleStatus",
            ),
        ],
        style={"width": "18rem"},
        color=bg_color,
        inverse=True
    )

    led_row = html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )
    # endregion


    # region LED Indicators for Clients Counts
    if client_counts['mongo'].shape[0] == client_counts['bq'].shape[0]:
        bg_color = 'success'
    else:
        bg_color = 'danger'
    clients_missing = client_counts['mongo'].shape[0] - client_counts['bq'].shape[0]
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("Clients Status", className="card-text", id='clientStatus')),
            dbc.CardImg(src="", bottom=True),
            dbc.Tooltip(
                f'mongo count: {client_counts["mongo"].shape[0]}, bigquery count: {client_counts["bq"].shape[0]}, missing: {clients_missing}',
                target="clientStatus",
            ),
        ],
        style={"width": "18rem"},
        color=bg_color,
        inverse=True
    )

    clients_row = html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )
    # endregion


    # region LED Indicators for Locations Counts
    if location_counts['mongo'] == location_counts['bq']:
        bg_color = 'success'
    else:
        bg_color = 'danger'
    locations_missing = location_counts['mongo'] - location_counts['bq']
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("Locations Status", className="card-text", id='locationStatus')),
            dbc.CardImg(src="", bottom=True),
            dbc.Tooltip(
                f'mongo count: {location_counts["mongo"]}, bigquery count: {location_counts["bq"]}, missing: {locations_missing} ',
                target="locationStatus",
            ),
        ],
        style={"width": "18rem"},
        color=bg_color,
        inverse=True
    )

    locations_row = html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )
    # endregion

    # region LED Indicators for Payments Counts
    if payments_locations_counts['mongo'] == payments_locations_counts['bq']:
        bg_color = 'success'
    else:
        bg_color = 'danger'
    payments_missing = payments_locations_counts['mongo'] - payments_locations_counts['bq']
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("Payments Status", className="card-text", id='paymentsStatus')),
            dbc.CardImg(src="", bottom=True),
            dbc.Tooltip(
                f'mongo count: {payments_locations_counts["mongo"]}, bigquery count: {payments_locations_counts["bq"]}, missing: {payments_missing}',
                target="paymentsStatus",
            ),
        ],
        style={"width": "18rem"},
        color=bg_color,
        inverse=True
    )

    payments_row = html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )
    # endregion

    # region LED Indicators for ItemsInCart Counts
    if items_locations_counts['mongo'] == items_locations_counts['bq']:
        bg_color = 'success'
    else:
        bg_color = 'danger'
    items_missing = items_locations_counts['mongo'] - items_locations_counts['bq']
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("ItemsInCart Status", className="card-text", id='itemsStatus')),
            dbc.CardImg(src="", bottom=True),
            dbc.Tooltip(
                f'mongo count: {items_locations_counts["mongo"]}, bigquery count: {items_locations_counts["bq"]}, missing: {items_missing}',
                target="itemsStatus",
            ),
        ],
        style={"width": "18rem"},
        color=bg_color,
        inverse=True
    )

    items_row = html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )
    # endregion


    # region LED Indicators for Discounts Counts
    if Discounts_locations_counts['mongo'] == Discounts_locations_counts['bq']:
        bg_color = 'success'
    else:
        bg_color = 'danger'
    Discounts_missing = Discounts_locations_counts['mongo'] - Discounts_locations_counts['bq']
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("Discounts Status", className="card-text", id='discountsStatus')),
            dbc.CardImg(src="", bottom=True),
            dbc.Tooltip(
                f'mongo count: {Discounts_locations_counts["mongo"]}, bigquery count: {Discounts_locations_counts["bq"]}, missing: {Discounts_missing}',
                target="discountsStatus",
            ),
        ],
        style={"width": "18rem"},
        color=bg_color,
        inverse=True
    )

    discounts_row = html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )
    # endregion


    # region LED Indicators for Customers Counts
    if Customers_locations_counts['mongo'] == Customers_locations_counts['bq']:
    # if 1805 == Customers_locations_counts['bq'].shape[0]:
        bg_color = 'success'
    else:
        bg_color = 'danger'
    Customers_missing = Customers_locations_counts['mongo'] - Customers_locations_counts['bq']
    # Customers_missing = 1805 - Customers_locations_counts['bq'].shape[0]
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("Customers Status", className="card-text", id='customersStatus')),
            dbc.CardImg(src="", bottom=True),
            dbc.Tooltip(
                f'mongo count: {Customers_locations_counts["mongo"]}, bigquery count: {Customers_locations_counts["bq"]}, missing: {Customers_missing}',
                # f'mongo count: {1805}, bigquery count: {Customers_locations_counts["bq"].shape[0]}, missing: {Customers_missing}',
                target="customersStatus",
            ),
        ],
        style={"width": "18rem"},
        color=bg_color,
        inverse=True
    )

    customers_row = html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )
    # endregion

    # region LED Indicators for InventoryActivities Counts
    if InventoryActivities_locations_counts['mongo'] == InventoryActivities_locations_counts['bq']:
    # if 1420 == InventoryActivities_locations_counts['bq'].shape[0]:
        bg_color = 'success'
    else:
        bg_color = 'danger'
    InventoryActivities_missing = InventoryActivities_locations_counts['mongo'] - InventoryActivities_locations_counts['bq']
    # InventoryActivities_missing = 1420 - InventoryActivities_locations_counts['bq'].shape[0]
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("InventoryActivity Status", className="card-text", id='inventoryActivitiesStatus')),
            dbc.CardImg(src="", bottom=True),
            dbc.Tooltip(
                f'mongo count: {InventoryActivities_locations_counts["mongo"]}, bigquery count: {InventoryActivities_locations_counts["bq"]}, missing: {InventoryActivities_missing}',
                # f'mongo count: {1420}, bigquery count: {InventoryActivities_locations_counts["bq"].shape[0]}, missing: {InventoryActivities_missing}',
                target="inventoryActivitiesStatus",
            ),
        ],
        style={"width": "18rem"},
        color=bg_color,
        inverse=True
    )

    inventoryActivities_row = html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )
    # endregion

    status_grid.add_element(led_row, 1, 1)
    status_grid.add_element(clients_row, 1, 2)
    status_grid.add_element(locations_row, 1, 3)
    status_grid.add_element(payments_row, 1, 4)
    status_grid.add_element(items_row, 2, 1)
    status_grid.add_element(discounts_row, 2, 2)
    status_grid.add_element(customers_row, 2, 3)
    status_grid.add_element(inventoryActivities_row, 2, 4)

    return status_grid



def old_etl_status():
    pos_date = metrics.get_pos_max_date('Sales')
    if pos_date >= datetime.today() - timedelta(days=3):
        bg_color = 'success'
    else:
        bg_color = 'danger'
    days_out = datetime.today() - pos_date
    bottom_card = dbc.Card(
        [
            dbc.CardBody(html.P("POS Sales", className="card-text", id='posStatus')),
            dbc.Tooltip(
                f'pos sales Max(CreatedAt): {pos_date}, How Many Days Old: {days_out}',
                target="posStatus",
            ),
        ],
        style={'width': '12rem'},
        color=bg_color,
        inverse=True
    )

    return html.Div([
        bottom_card
    ], className='d-flex flex-row justify-content-between align-items-center'
    )

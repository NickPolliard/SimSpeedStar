import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

categories_header = dbc.Row([
    dbc.Col('Legacy Software Category', width=4),
    dbc.Col('Flowhub Category', width=4)
]),

product_columns_header = dbc.Row([
    dbc.Col('Legacy Software Column', width=3),
    dbc.Col('Flowhub Column', width=3),
    dbc.Col('Applies to', width=2),
    dbc.Col('Identification', width=2),
]),

strain_columns_header = dbc.Row([
    dbc.Col('Legacy Software Column', width=4),
    dbc.Col('Flowhub Column', width=4),
]),

inventory_columns_header = dbc.Row([
    dbc.Col('Legacy Software Column', width=3),
    dbc.Col('Flowhub Column', width=3),
    dbc.Col('Applies to', width=2),
    dbc.Col('Identification', width=2),
]),

headers = {
    'categories_header': categories_header,
    'product_columns_header': product_columns_header,
    'strain_columns_header': strain_columns_header,
    'inventory_columns_header': inventory_columns_header
}


def get_competitor_list(saved_setup, matching_store):
    mapped_list = list(zip(*matching_store['categories_mapping']))
    if mapped_list:
        competitor_categories = [c for c in saved_setup['competitor_categories'] if c not in mapped_list[0]]
    else:
        competitor_categories = saved_setup['competitor_categories']

    return competitor_categories


def get_column_list(saved_setup, column_type):
    column_list = saved_setup['columns'][column_type]
    column_list = list(set(column_list))
    column_list.sort()
    return column_list


def generate_dropdows(n_clicks, card_type, saved_setup, matching_store):
    if card_type == 'categories':
        # Getting the list of competitor categories that have not been mapped yet
        competitor_categories = get_competitor_list(saved_setup, matching_store)
        dropdown_row = dbc.Row([
            dbc.Col([
                dcc.Dropdown(id={'type': f'competitor-{card_type}-dropdown', 'index': n_clicks},
                             options=[{'label': i, 'value': i} for i in competitor_categories])
            ], width=4),
            dbc.Col([
                dcc.Dropdown(id={'type': f'fh-{card_type}-dropdown', 'index': n_clicks},
                             options=[{'label': i, 'value': i} for i in saved_setup['fh_categories']])
            ], width=4),
            dbc.Col([
                dbc.Button('Remove Row', id={'type': f'{card_type}-remove-row', 'index': n_clicks}, color='bare')
            ])
        ], id={'type': f'{card_type}-dropdowns-row', 'index': n_clicks}, className='my-2')
    elif card_type == 'strain-columns':
        column_type = card_type.split('-')[0]
        dropdown_row = dbc.Row([
            dbc.Col([
                dcc.Dropdown(id={'type': f'competitor-{card_type}-dropdown', 'index': n_clicks},
                             options=[{'label': i, 'value': i} for i in get_column_list(saved_setup, 'competitor')])
            ], width=4),
            dbc.Col([
                dcc.Dropdown(id={'type': f'fh-{card_type}-dropdown', 'index': n_clicks},
                             options=[{'label': i, 'value': i} for i in get_column_list(saved_setup, column_type)])
            ], width=4),
            dbc.Col([
                dbc.Button('Remove Row', id={'type': f'{card_type}-remove-row', 'index': n_clicks}, color='bare')
            ])
        ], id={'type': f'{card_type}-dropdowns-row', 'index': n_clicks}, className='my-2')
    else:
        column_type = card_type.split('-')[0]
        fh_categories = saved_setup['fh_categories']
        fh_categories.remove('Strains')
        fh_categories.insert(0, 'All')
        dropdown_row = dbc.Row([
            dbc.Col([
                dcc.Dropdown(id={'type': f'competitor-{card_type}-dropdown', 'index': n_clicks},
                             options=[{'label': i, 'value': i} for i in get_column_list(saved_setup, 'competitor')])
            ], width=3),
            dbc.Col([
                dcc.Dropdown(id={'type': f'fh-{card_type}-dropdown', 'index': n_clicks},
                             options=[{'label': i, 'value': i} for i in get_column_list(saved_setup, column_type)])
            ], width=3),
            dbc.Col([
                dcc.Dropdown(id={'type': f'applies-{card_type}-dropdown', 'index': n_clicks},
                             options=[{'label': i, 'value': i} for i in fh_categories])
            ], width=2),
            dbc.Col([
                dcc.Dropdown(id={'type': f'identification-{card_type}-dropdown', 'index': n_clicks},
                             options=[{'label': i, 'value': i} for i in ['Generic', 'Product Name', 'Price', 'Cost', 'Weight Unit']])
            ], width=2),
            dbc.Col([
                dbc.Button('Remove Row', id={'type': f'{card_type}-remove-row', 'index': n_clicks}, color='bare')
            ])
        ], id={'type': f'{card_type}-dropdowns-row', 'index': n_clicks}, className='my-2')
    return dropdown_row

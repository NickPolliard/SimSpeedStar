import json
import os

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import dapp
from apps import status, locationAnalysis, locationsDetail, stakeholder

dapp.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@dapp.callback(Output('page-content', 'children'),
               [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return status.layout
#    elif pathname == '/status':
#        return status.layout
#    elif pathname == '/locationAnalysis':
#        return locationAnalysis.layout
#    elif pathname == '/locationsDetail':
#        return locationsDetail.layout
#    elif pathname == '/stakeholder':
#        return stakeholder.layout
    else:
        return '404: Page not found'


@dapp.server.route("/ping")
def ping():
    return "{status: ok}"


@dapp.server.route("/version")
def version():
    with open('version.json') as json_file:
        data = json.load(json_file)
    return data


# start Flask server
if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT') == 'dev':
        debug = True
    else:
        debug = False

    print('Run server')
    dapp.run_server(
        debug=debug,
        host='0.0.0.0',
        port=8050
    )

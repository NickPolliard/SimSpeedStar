import dash_bootstrap_components as dbc
import dash_html_components as html

from app import dapp


def banner():
    banner = dbc.Nav([
        html.Div(html.Img(src=dapp.get_asset_url("Flowhub_Logo_Icon.svg"), style={'height': '1.5rem'}),
                 className='ml-2 mr-4 py-1'),
        html.Div(['Stakeholder Dashboard'], className='p-2'),
    ], className='banner p-2')
    return banner


def navbar(current_page):

    navbar = dbc.Nav([
        dbc.NavItem(dbc.NavLink("Home", active=True, href="/stakeholder", className='px-2')),


    ])
    return navbar

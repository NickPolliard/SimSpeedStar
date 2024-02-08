import dash_bootstrap_components as dbc
import dash_html_components as html

from app import dapp


def banner():
    banner = dbc.Nav([
        html.Div(html.Img(src=dapp.get_asset_url("Flowhub_Logo_Icon.svg"), style={'height': '1.5rem'}),
                 className='ml-2 mr-4 py-1'),
        html.Div(['MatchStick Pro Max X Dashboard'], className='p-2'),
    ], className='banner p-2')
    return banner


def navbar(current_page):
    navbar = dbc.Nav([
        dbc.NavItem(dbc.NavLink("Dashboard", active=True, href="/", className='px-2')),
        dbc.NavItem(dbc.NavLink("Manual Match", active=True, href="/manualMatch", className='px-2')),
        dbc.NavItem(dbc.NavLink("Known Population", active=True, href="/knownPopulation", className='px-2')), 
        dbc.NavItem(dbc.NavLink("Page 3", active=True, href="/page_3", className='px-2')), 
    ])
    return navbar

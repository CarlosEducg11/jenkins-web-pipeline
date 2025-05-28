import pandas as pd
from dash import Dash, html, Input, Output, callback_context, dcc
import dash_bootstrap_components as dbc

from pages.home import render as render_home
from pages.dados import render as render_dados
from pages.modelos import render as render_modelos
from pages.config import render as render_config

# Custom colors
sidebar_bg = "#f8f9fa"
text_color = "#495057"
hover_color = "#e9ecef"
active_bg_color = "#7f8996"
active_text_color = "white"
clicked_color = "#bac3cc"

# Sidebar with logo image instead of icons
logo_path = '/assets/sea-level.png'
logo_home = '/assets/sea-level.png'
logo_dados = '/assets/sea-level.png'
logo_modelos = '/assets/sea-level.png'
logo_config = '/assets/sea-level.png'

def navlink_with_logo(text, href, id_, logo, active=False):
    return dbc.NavLink(
        [
            html.Img(src=logo, style={'width': '20px', 'marginRight': '8px'}),
            text
        ],
        href=href,
        id=id_,
        active=active,
        style={
            "fontSize": "0.9rem",
            "color": text_color,
            "display": "flex",
            "alignItems": "center",
            "padding": "0.5rem 1rem",
            "userSelect": "none",
        },
        className="custom-nav-link"
    )

sidebar = html.Div(
    [
        html.Div(
            html.Img(src='/assets/sea-level.png', style={'width': '80px', 'marginBottom': '1rem', 'alignSelf': 'center'}),
            style={'textAlign': 'center'}
        ),
        navlink_with_logo("Home", "#home", "home-link", logo_home, active=True),
        navlink_with_logo("Dados", "#dados", "dados-link", logo_dados),
        navlink_with_logo("Modelos", "#modelos", "modelos-link", logo_modelos),
        navlink_with_logo("Configurações", "#config", "config-link", logo_config),
        
        html.Div(
            [
                html.Img(src='/assets/table.png', style={'width': '40px', 'height': '40px', 'marginRight': '5px'}),
                html.Span(id='total-rows-text', style={
                    'fontWeight': 'bold',
                    'fontSize': '1.8rem',
                    'color': text_color,
                }),
            ],
            style={
                'padding': '1rem',
                'marginTop': 'auto',
                'display': 'flex',
                'justifyContent': 'center',  # center horizontally
                'alignItems': 'center',      # center vertically
                'userSelect': 'none',
                'gap': '7px',               # space between icon and number
            }
        ),

        dcc.Interval(id='interval-refresh', interval=10*1000, n_intervals=0)
    ],
    style={
        "height": "100vh",
        "padding": "1rem 0.5rem",
        "width": "180px",
        "boxShadow": "2px 0 5px rgba(0,0,0,0.1)",
        "overflowX": "hidden",
        "backgroundColor": sidebar_bg,
        "display": "flex",
        "flexDirection": "column",
    },
    className="bg-white",
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col(html.Div(id='tab-content', style={'marginTop': '20px'}), width=10)
    ]),
    fluid=True,
)

@app.callback(
    Output('tab-content', 'children'),
    Output('home-link', 'active'),
    Output('dados-link', 'active'),
    Output('modelos-link', 'active'),
    Output('config-link', 'active'),
    Input('home-link', 'n_clicks'),
    Input('dados-link', 'n_clicks'),
    Input('modelos-link', 'n_clicks'),
    Input('config-link', 'n_clicks'),
)
def render_tab_content(home, dados, modelos, config):
    ctx = callback_context
    tab_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'home-link'

    return {
        'home-link': (render_home(), True, False, False, False),
        'dados-link': (render_dados(), False, True, False, False),
        'modelos-link': (render_modelos(), False, False, True, False),
        'config-link': (render_config(), False, False, False, True),
    }[tab_id]

# 🔁 Callback to update total rows dynamically
@app.callback(
    Output('total-rows-text', 'children'),
    Input('interval-refresh', 'n_intervals')
)
def update_total_rows(n):
    try:
        df = pd.read_csv('dadosAlagamentoPI.csv', sep=',', encoding='latin-1')
        return str(len(df))  # just the number, icon is fixed in sidebar
    except Exception:
        return "Error"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
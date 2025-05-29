import os
import pandas as pd
from dash import Dash, html, Input, Output, callback_context, dcc
import dash_bootstrap_components as dbc

# Sidebar colors and icons
sidebar_bg = "#f8f9fa"
text_color = "#495057"

logo_home = '/assets/icons/data-lake.png'
logo_dados = '/assets/icons/rating.png'
logo_modelos = '/assets/icons/bar-chart.png'
logo_config = '/assets/icons/develop.png'

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
            [
                html.Img(src='/assets/icons/ocean.gif', style={'width': '80px', 'marginBottom': '0.5rem'}),
                html.Hr(style={'borderTop': '3px solid #444444', 'margin': '0.5rem 1rem'})
            ],
            style={'textAlign': 'center'}
        ),

        navlink_with_logo("Datalake", "#home", "home-link", logo_home, active=True),
        navlink_with_logo("Spark", "#dados", "dados-link", logo_dados),
        navlink_with_logo("Modelos", "#modelos", "modelos-link", logo_modelos),
        navlink_with_logo("Hadoop", "#config", "config-link", logo_config),

        html.Div(
            [
                dbc.Button(
                    [
                        html.Img(
                            src="/assets/icons/refresh.png",
                            style={
                                "height": "18px",
                                "width": "18px",
                                "marginRight": "8px"
                            }
                        ),
                        "Refresh"
                    ],
                    id="refresh-button",
                    color="light",  # Bootstrap fallback
                    size="md",
                    style={
                        'width': '100%',
                        'marginBottom': '15px',
                        'borderRadius': '8px',
                        'backgroundColor': '#555555',  # Light gray in HEX
                        'border': '1px solid #888',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.08)',
                        'fontWeight': '700',
                        'fontSize': '1rem',
                        'fontFamily': 'Segoe UI, Roboto, sans-serif',
                        'color': '#ffffff',  # White text
                        'cursor': 'pointer',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'gap': '6px',
                        'transition': 'background-color 0.2s ease-in-out',
                    }
                ),

                html.Hr(style={'borderTop': '3px solid #444444', 'margin': '0 1rem 0.5rem 1rem'}),

                html.Div(
                    [
                        html.Img(src='/assets/icons/table.png', style={'width': '40px', 'height': '40px', 'marginRight': '5px'}),
                        html.Span(id='total-rows-text', style={
                            'fontWeight': 'bold', 'fontSize': '1.8rem', 'color': text_color,
                        }),
                    ],
                    style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '7px'}
                )
            ],
            style={'padding': '1rem', 'marginTop': 'auto', 'userSelect': 'none'}
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "height": "100vh",
        "padding": "1rem 0.5rem",
        "width": "180px",
        "boxShadow": "2px 0 5px rgba(0,0,0,0.1)",
        "overflowX": "hidden",
        "backgroundColor": sidebar_bg,
        "display": "flex",
        "flexDirection": "column",
        "zIndex": 1000
    },
    className="bg-white",
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    sidebar,
    dcc.Loading(
        id="loading-tab-content",
        type="circle",
        children=html.Div(
            id='tab-content',
            style={
                'marginLeft': '180px',
                'padding': '20px',
                'overflowY': 'auto',
                'height': '100vh',
            }
        ),
        style={'marginLeft': '180px', 'height': '100vh', 'overflowY': 'auto'}
    )
])

# Page content and navlink states — also triggered by refresh button
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
    Input('refresh-button', 'n_clicks')  # <- added refresh here
)
def update_page_content(home_clicks, dados_clicks, modelos_clicks, config_clicks, refresh_clicks):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'home-link'

    clicks = {
        'home-link': home_clicks or 0,
        'dados-link': dados_clicks or 0,
        'modelos-link': modelos_clicks or 0,
        'config-link': config_clicks or 0
    }

    # Find active tab based on last clicked or fallback to home
    max_clicked = max(clicks.values())
    active_tabs = [tab for tab, count in clicks.items() if count == max_clicked]
    active_tab = active_tabs[0] if active_tabs else 'home-link'

    if active_tab == 'home-link':
        from pages.datalake import render as render_home
        content = render_home()
    elif active_tab == 'dados-link':
        from pages.spark import render as render_dados
        content = render_dados()
    elif active_tab == 'modelos-link':
        from pages.modelos import render as render_modelos
        content = render_modelos()
    elif active_tab == 'config-link':
        from pages.hadoop import render as render_config
        content = render_config()
    else:
        content = html.Div("Page not found")

    return (
        content,
        active_tab == 'home-link',
        active_tab == 'dados-link',
        active_tab == 'modelos-link',
        active_tab == 'config-link',
    )

# Manual refresh of total rows via refresh button
@app.callback(
    Output('total-rows-text', 'children'),
    Input('refresh-button', 'n_clicks'),
    prevent_initial_call=True
)
def update_total_rows(n_clicks):
    file_path = 'data/dadosCorretosPI.csv'
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, sep=',', encoding='latin-1')
            return str(len(df))
        except Exception:
            return "Error"
    else:
        return "0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
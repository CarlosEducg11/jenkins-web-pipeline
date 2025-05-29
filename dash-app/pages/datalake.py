# page_olap.py

import os
import sqlite3
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, callback

def render():
    return html.Div([
        html.H3("Dados"),
        html.P("Aqui você pode mostrar tabelas, filtros e visualizações relacionadas a dados."),
])
'''
CSV_PATH = 'assets/dadosCorretosPI.csv'
DATALAKE_PATH = 'assets/datalake'
DW_PATH = 'assets/datawarehouse.db'

# ETL runs once at import
def etl_process():
    if not os.path.exists(DW_PATH):
        df = pd.read_csv(CSV_PATH, encoding='latin-1')

        dim_vazao = df[['Unnamed: 0', 'vazaoMedia', 'vazaoAtual']]
        dim_mililitro = df[['Unnamed: 0', 'milimitroHora', 'milimitroDia', 'milimitroSeteDias']]
        fato = df[['Unnamed: 0', 'alagou']]

        os.makedirs(DATALAKE_PATH, exist_ok=True)
        dim_vazao.to_csv(f'{DATALAKE_PATH}/dim_vazao.csv', index=True)
        dim_mililitro.to_csv(f'{DATALAKE_PATH}/dim_mililitro.csv', index=True)
        fato.to_csv(f'{DATALAKE_PATH}/fato.csv', index=True)

        conn = sqlite3.connect(DW_PATH)
        dim_vazao.to_sql('dim_vazao', conn, if_exists='replace', index=True)
        dim_mililitro.to_sql('dim_mililitro', conn, if_exists='replace', index=True)
        fato.to_sql('fato', conn, if_exists='replace', index=True)
        conn.close()

etl_process()

olap_dimensoes = {
    'vazaoMedia': 't."vazaoMedia"',
    'vazaoAtual': 't."vazaoAtual"',
    'alagou': 'f."alagou"',
}

def render():
    return html.Div([
        html.H3("Consulta OLAP Interativa"),
        html.Div([
            dcc.Dropdown(
                id='dim1-dropdown',
                options=[{'label': k, 'value': k} for k in olap_dimensoes.keys()],
                value='vazaoMedia',
                clearable=False,
                style={'width': '300px', 'display': 'inline-block'}
            ),
            dcc.Dropdown(
                id='dim2-dropdown',
                options=[{'label': 'Nenhuma', 'value': 'Nenhuma'}] + [{'label': k, 'value': k} for k in olap_dimensoes.keys()],
                value='Nenhuma',
                clearable=False,
                style={'width': '300px', 'display': 'inline-block', 'marginLeft': '20px'}
            ),
        ], style={'marginBottom': '20px'}),

        dcc.Loading(
            id='loading-olap',
            children=[dcc.Graph(id='olap-bar-chart')],
            type='circle'
        ),
    ], style={'padding': '20px'})


# If this module is imported in your main app,
# you can register callbacks here:
def register_callbacks(app):

    @app.callback(
        Output('olap-bar-chart', 'figure'),
        Input('dim1-dropdown', 'value'),
        Input('dim2-dropdown', 'value'),
    )
    def gerar_consulta(dim1, dim2):
        conn = sqlite3.connect(DW_PATH)
        col1 = olap_dimensoes[dim1]
        col2 = olap_dimensoes[dim2] if dim2 != 'Nenhuma' else None

        select_clause = f"{col1} AS dim1"
        group_clause = "dim1"

        if col2:
            select_clause += f", {col2} AS dim2"
            group_clause += ", dim2"

        query = f"""
            SELECT {select_clause}, AVG(t."vazaoMedia") AS media
            FROM fato f
            JOIN dim_vazao t ON f."Unnamed: 0" = t."Unnamed: 0"
            GROUP BY {group_clause}
            ORDER BY media DESC
            LIMIT 100
        """
        df_resultado = pd.read_sql_query(query, conn)
        conn.close()

        if col2:
            fig = px.bar(df_resultado, x='dim1', y='media', color='dim2', barmode='group')
        else:
            fig = px.bar(df_resultado, x='dim1', y='media')

        fig.update_layout(title=f'Consulta OLAP: {dim1}' + (f' e {dim2}' if col2 else ''),
                          xaxis_title=dim1,
                          yaxis_title='Média Vazão')
        return fig'''

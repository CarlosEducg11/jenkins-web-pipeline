import os
<<<<<<< HEAD
import sqlite3
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output, callback

CSV_PATH = 'data/dadosCorretosPI.csv'
DATALAKE_PATH = 'data/datalake'
DW_PATH = 'data/datawarehouse.db'

# ETL process to load data into data lake and warehouse
def etl_process():
    if not os.path.exists(DW_PATH):
        df = pd.read_csv(CSV_PATH, encoding='latin-1')

        # Ensure we have a stable ID column for joining
        df['id'] = df.index

        dim_vazao = df[['id', 'vazaoMedia', 'vazaoAtual']]
        dim_mililitro = df[['id', 'milimitroHora', 'milimitroDia', 'milimitroSeteDias']]
        fato = df[['id', 'alagou']]

        os.makedirs(DATALAKE_PATH, exist_ok=True)
        dim_vazao.to_csv(f'{DATALAKE_PATH}/dim_vazao.csv', index=False)
        dim_mililitro.to_csv(f'{DATALAKE_PATH}/dim_mililitro.csv', index=False)
        fato.to_csv(f'{DATALAKE_PATH}/fato.csv', index=False)

        conn = sqlite3.connect(DW_PATH)
        dim_vazao.to_sql('dim_vazao', conn, if_exists='replace', index=False)
        dim_mililitro.to_sql('dim_mililitro', conn, if_exists='replace', index=False)
        fato.to_sql('fato', conn, if_exists='replace', index=False)
        conn.close()

etl_process()

# OLAP dimension options (column -> SQL reference)
=======
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import sqlite3

# Constants
CSV_PATH = 'data/dadosCorretosPI.csv'
DW_PATH = 'data/datawarehouse.db'

# OLAP function to query the data
>>>>>>> 1a39fbc (a)
olap_dimensoes = {
    'vazaoMedia': 't."vazaoMedia"',
    'vazaoAtual': 't."vazaoAtual"',
    'alagou': 'f."alagou"',
}

<<<<<<< HEAD
# Layout for the OLAP page
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


# Register callbacks (called from app.py)
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
            JOIN dim_vazao t ON f.id = t.id
            GROUP BY {group_clause}
            ORDER BY media DESC
            LIMIT 100
        """

        df_resultado = pd.read_sql_query(query, conn)
        conn.close()

        # Debugging tip (optional): print(df_resultado.head())

        if df_resultado.empty:
            fig = px.bar(title="Nenhum dado disponível para os filtros selecionados.")
        else:
            if col2:
                fig = px.bar(df_resultado, x='dim1', y='media', color='dim2', barmode='group')
            else:
                fig = px.bar(df_resultado, x='dim1', y='media')

            fig.update_layout(
                title=f'Consulta OLAP: {dim1}' + (f' e {dim2}' if col2 else ''),
                xaxis_title=dim1,
                yaxis_title='Média Vazão'
            )

        return fig
=======
def run_olap_query(dim1, dim2):
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
        ORDER BY f."alagou" DESC
        LIMIT 100
    """
    df_result = pd.read_sql_query(query, conn)
    conn.close()
    return df_result

# Function to generate clustering plot
def cluster_plot():
    df = pd.read_csv(CSV_PATH, encoding='latin-1')
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[['vazaoMedia', 'vazaoAtual']])
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['Cluster'] = kmeans.fit_predict(scaled_data)

    fig = px.scatter(df, x='vazaoMedia', y='vazaoAtual', color='Cluster',
                     title='Clusters de Alagamentos', labels={'vazaoMedia': 'Vazão Média', 'vazaoAtual': 'Vazão Atual'})
    return fig

# Function to generate distribution plot
def distribution_plot():
    df = pd.read_csv(CSV_PATH, encoding='latin-1')
    fig = px.histogram(df, x='vazaoMedia', nbins=30, title='Distribuição da Vazão Média', marginal="box", color_discrete_sequence=['skyblue'])
    fig.update_layout(xaxis_title='Vazão Média', yaxis_title='Frequência')
    return fig

# Home page layout
def render():
    return html.Div([
        html.H2("Painel de Análise - OLAP & Clustering"),
        dbc.Row([
            dbc.Col([
                html.Label("Dimensão 1"),
                dcc.Dropdown(id='dim1', options=[{'label': k, 'value': k} for k in olap_dimensoes.keys()], value='vazaoMedia')
            ], width=6),
            dbc.Col([
                html.Label("Dimensão 2 (opcional)"),
                dcc.Dropdown(id='dim2', options=[{'label': 'Nenhuma', 'value': 'Nenhuma'}] + [{'label': k, 'value': k} for k in olap_dimensoes.keys()],
                             value='Nenhuma')
            ], width=6),
        ], className='my-3'),

        dcc.Graph(id='olap-graph'),

        html.Hr(),

        html.H4("Clusters de Alagamento"),
        dcc.Graph(figure=cluster_plot()),

        html.Hr(),

        html.H4("Distribuição da Vazão Média"),
        dcc.Graph(figure=distribution_plot()),
    ])
>>>>>>> 1a39fbc (a)

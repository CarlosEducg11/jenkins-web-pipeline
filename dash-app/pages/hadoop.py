import pandas as pd
from dash import html, dcc, dash_table

def render():
    return html.Div([
        html.H3("Dados"),
        html.P("Aqui você pode mostrar tabelas, filtros e visualizações relacionadas a dados."),
])
'''
def simulate_hadoop():
    df = pd.read_csv('assets/dadosCorretosPI.csv', sep=',', encoding='latin-1')

    # --- MapReduce ---
    def mapper(linhas):
        pares = []
        for linha in linhas:
            if pd.notna(linha):
                for solo in linha.replace("[", "").replace("]", "").replace("'", "").split(","):
                    pares.append((solo.strip(), 1))
        return pares

    def shuffle(mapped_data):
        agrupado = {}
        for chave, valor in mapped_data:
            agrupado.setdefault(chave, []).append(valor)
        return agrupado

    def reducer(agrupado):
        return {chave: sum(valores) for chave, valores in agrupado.items()}

    mapeado = mapper(df["solo"])
    agrupado = shuffle(mapeado)
    resultado_mapreduce = reducer(agrupado)
    mapreduce_df = pd.DataFrame(list(resultado_mapreduce.items()), columns=["Solo", "Ocorrências"]).sort_values(by="Ocorrências", ascending=False)

    # --- Hive (SQL-style) ---
    hive_df = df[["vazaoMedia", "vazaoAtual", "alagou"]]
    hive_filtered = hive_df[hive_df["vazaoAtual"] > hive_df["vazaoMedia"]].copy()

    # --- Pig (Transformation Logic) ---
    dados_pig = df[["vazaoMedia", "vazaoAtual", "alagou"]].dropna().head(100).values.tolist()
    valor = 2
    dados_pig = [[item * valor for item in row] for row in dados_pig]
    filtrado = [x for x in dados_pig if x[1] > x[0]]
    transformed_pig = [(str(x[0]), str(x[1]), bool(x[2])) for x in filtrado]
    pig_df = pd.DataFrame(transformed_pig, columns=["Vazão Média", "Vazão Atual", "Alagou"])

    # --- HBase (Column-oriented simulated store) ---
    hbase = {
        f"Rio: {i}": {
            "Vazão Média": int(row["vazaoMedia"]),
            "Vazão Atual": int(row["vazaoAtual"]),
            "Alagou": bool(row["alagou"])
        }
        for i, row in df.iterrows() if pd.notna(row["vazaoMedia"]) and pd.notna(row["vazaoAtual"])
    }
    hbase_df = pd.DataFrame([
        {"Rio": chave, **valores} for chave, valores in hbase.items()
    ])

    return mapreduce_df, hive_filtered, pig_df, hbase_df


def render():
    mapreduce_df, hive_df, pig_df, hbase_df = simulate_hadoop()

    return html.Div([
        html.H2("🛠️ Simulação de Hadoop com Pandas"),

        html.H4("🧮 MapReduce - Contagem de Tipos de Solo"),
        dash_table.DataTable(
            data=mapreduce_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in mapreduce_df.columns],
            style_table={'overflowX': 'auto'},
            page_size=10
        ),

        html.H4("📊 Hive - Vazões Onde a Atual > Média"),
        dash_table.DataTable(
            data=hive_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in hive_df.columns],
            style_table={'overflowX': 'auto'},
            page_size=10
        ),

        html.H4("🐷 Pig - Vazão Atual Duas Vezes Acima da Média"),
        html.P(f"Total filtrado: {len(pig_df)} registros"),
        dash_table.DataTable(
            data=pig_df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in pig_df.columns],
            style_table={'overflowX': 'auto'},
            page_size=10
        ),

        html.H4("🏛️ HBase - Banco Colunar Simulado"),
        dash_table.DataTable(
            data=hbase_df.head(20).to_dict('records'),
            columns=[{"name": i, "id": i} for i in hbase_df.columns],
            style_table={'overflowX': 'auto'},
            page_size=10
        ),
    ], style={"padding": "30px"})'''

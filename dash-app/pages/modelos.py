from dash import html

def render_image_section(title, description, image_path):
    return html.Div([
        html.H3(title, style={'marginBottom': '10px'}),
        html.P(description, style={'marginBottom': '20px'}),
        html.Img(src=image_path, style={
            'width': '100%',
            'maxWidth': '1000px',  # ⚖️ Perfect balance
            'display': 'block',
            'marginLeft': 'auto',
            'marginRight': 'auto',
            'border': '1px solid #ccc',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.05)',
            'borderRadius': '8px'
        }),
    ], style={
        'backgroundColor': '#f9f9f9',
        'padding': '30px',
        'marginBottom': '40px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
        'textAlign': 'center'
    })

def render():
    return html.Div([
        render_image_section(
            "📊 Tabela de Dados",
            "Visualização da tabela de dados utilizada na análise.",
            "/data/tabela_dados.png"
        ),
        render_image_section(
            "📉 Matriz de Confusão",
            "Resultado da matriz de confusão do modelo de classificação.",
            "/data/matriz_confusao.png"
        ),
        render_image_section(
            "🔍 Gráfico de Clusters",
            "Visualização dos clusters gerados pelo algoritmo.",
            "/data/grafico_cluster.png"
        ),
        render_image_section(
            "📈 Relatório de Regressão",
            "Resumo dos resultados do modelo de regressão.",
            "/data/relatorio_regressao.png"
        ),
    ], style={'padding': '60px', 'maxWidth': '1200px', 'margin': '0 auto'})

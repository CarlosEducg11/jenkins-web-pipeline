import pandas as pd
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import plotly.graph_objects as go

# Load data
df = pd.read_csv('data/dadosAlagamentoPI.csv', sep=',', encoding='latin-1')

print(df.columns)

# Prepare data
X = df.drop(columns=['Unnamed: 0', 'Alagou'], errors='ignore')
y = df['Alagou']

numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object', 'category']).columns

numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=69)

model = RandomForestClassifier(n_estimators=100, random_state=69)
pipeline = Pipeline([('preprocessor', preprocessor), ('classifier', model)])
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
classes = ['Classe 0', 'Classe 1']

# Create Plotly heatmap for confusion matrix
fig = go.Figure(data=go.Heatmap(
    z=cm,
    x=classes,
    y=classes,
    colorscale='Blues',
    text=cm,
    texttemplate="%{text}",
    hoverongaps=False
))

fig.update_layout(
    title='Matriz de Confusão',
    xaxis_title='Previsão',
    yaxis_title='Verdadeiro',
    yaxis_autorange='reversed'
)

# After loading the data
row_count = len(df)

# Then in the sidebar, add a new html.Div to show it
sidebar = dbc.Nav(
    [
        html.Div(
            html.Img(src='/assets/sea-level.png', style={'width': '80px', 'margin-bottom': '1rem'}),
            style={'textAlign': 'center'}
        ),
        html.Div(f'Total rows: {row_count}', style={'padding': '0.5rem 1rem', 'fontWeight': 'bold', 'fontSize': '0.9rem'}),
        dbc.NavLink("Home", href="#", active="exact", style={"fontSize": "0.9rem"}),
        dbc.NavLink("Dados", href="#dados", active="exact", style={"fontSize": "0.9rem"}),
        dbc.NavLink("Modelos", href="#modelos", active="exact", style={"fontSize": "0.9rem"}),
        dbc.NavLink("Configurações", href="#config", active="exact", style={"fontSize": "0.9rem"}),
    ],
    vertical=True,
    pills=True,
    className="bg-white",
    style={
        "height": "100vh",
        "padding": "1rem 0.5rem",
        "width": "150px",
        "boxShadow": "2px 0 5px rgba(0,0,0,0.1)",
        "overflowX": "hidden",
    }
)


# Dash app with sidebar and content
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col([
            html.H1("Matriz de Confusão Interativa"),
            dcc.Graph(figure=fig)
        ], width=10)
    ]),
    fluid=True,
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, ctx

# Charger les données simulées
df = pd.read_csv('esg_simule.csv')

# Initialiser l'app Dash
app = Dash(__name__)
server = app.server  # Pour Render

app.title = "GreenCircle ESG Prototype"

app.layout = html.Div(style={
    'fontFamily': 'Arial',
    'backgroundColor': '#F4F9F4',
    'padding': '20px'
}, children=[

    html.H1("🌿 GreenCircle - Plateforme ESG locale", style={
        'color': '#2F4F4F',
        'textAlign': 'center',
        'fontSize': '36px',
        'marginBottom': '30px'
    }),

    html.Div([
        html.Label("🔍 Filtrer par ville :", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='ville-dropdown',
            options=[{'label': ville, 'value': ville} for ville in sorted(df['Ville'].unique())],
            placeholder="Sélectionner une ville",
            style={'width': '300px', 'marginBottom': '10px'}
        ),
        html.Button("🔄 Réinitialiser", id='reset-button', n_clicks=0, style={'marginLeft': '10px'})
    ]),

    html.Div(style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'space-between',
        'marginTop': '20px'
    }, children=[

        html.Div(style={
            'flex': '1',
            'minWidth': '40%',
            'height': '70vh',
            'marginRight': '20px',
            'backgroundColor': 'rgba(255, 255, 255, 0.8)',
            'borderRadius': '15px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'padding': '10px'
        }, children=[
            html.H3("🗺️ Carte ESG", style={'textAlign': 'center', 'color': '#3B7A57'}),
            dcc.Graph(id='map', style={
                'height': '60vh'
            })
        ]),

        html.Div(style={
            'flex': '1',
            'minWidth': '40%',
            'height': '70vh',
            'backgroundColor': '#FFFFFF',
            'borderRadius': '15px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'padding': '10px'
        }, children=[
            html.H3("🏙️ Top 10 villes par Score ESG", style={
                'textAlign': 'center',
                'color': '#3B7A57'
            }),
            dcc.Graph(id='bar-chart', style={
                'height': '60vh'
            })
        ])
    ]),

    html.Div(style={
        'marginTop': '30px',
        'backgroundColor': '#FFFFFF',
        'borderRadius': '15px',
        'padding': '20px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }, children=[
        html.H3("🌱 Corrélation Végétalisation et Recyclage", style={
            'textAlign': 'center',
            'color': '#3B7A57'
        }),
        dcc.Graph(id='scatter-plot')
    ])
])

# Callback pour la carte
@app.callback(
    Output('map', 'figure'),
    Input('ville-dropdown', 'value'),
    Input('reset-button', 'n_clicks')
)
def update_map(selected_ville, reset_clicks):
    triggered_id = ctx.triggered_id
    if triggered_id == 'reset-button' or not selected_ville:
        filtered_df = df
    else:
        filtered_df = df[df['Ville'] == selected_ville]

    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude", lon="Longitude",
        color="Score_ESG",
        size="Vegetalisation_%",
        hover_name="Zone",
        custom_data=["Zone"],
        zoom=5,
        height=600,
        color_continuous_scale="Greens"
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# Callback pour le graphique à barres
@app.callback(
    Output('bar-chart', 'figure'),
    Input('ville-dropdown', 'value'),
    Input('reset-button', 'n_clicks')
)
def update_bar_chart(selected_ville, reset_clicks):
    triggered_id = ctx.triggered_id
    if triggered_id == 'reset-button' or not selected_ville:
        grouped_df = df.groupby('Ville')['Score_ESG'].mean().nlargest(10).reset_index()
    else:
        grouped_df = df[df['Ville'] == selected_ville].groupby('Ville')['Score_ESG'].mean().reset_index()

    fig = px.bar(
        grouped_df,
        x='Score_ESG',
        y='Ville',
        orientation='h',
        color='Score_ESG',
        color_continuous_scale='Greens'
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=500, margin=dict(l=0, r=0, t=20, b=0))
    return fig

# Callback pour le scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('ville-dropdown', 'value'),
    Input('reset-button', 'n_clicks')
)
def update_scatter(selected_ville, reset_clicks):
    triggered_id = ctx.triggered_id
    if triggered_id == 'reset-button' or not selected_ville:
        scatter_df = df
    else:
        scatter_df = df[df['Ville'] == selected_ville]

    fig = px.scatter(
        scatter_df,
        x='Vegetalisation_%',
        y='Recyclage_%',
        color='Ville',
        hover_name='Zone',
        size='Score_ESG',
        title='Végétalisation vs Recyclage',
        height=500
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    return fig

if __name__ == '__main__':
    app.run(debug=True)



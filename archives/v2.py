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
        dcc.Graph(id='map', style={
            'width': '100%',
            'height': '60vh',
            'borderRadius': '15px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'marginBottom': '30px'
        }),

        html.Div(style={
            'backgroundColor': '#FFFFFF',
            'borderRadius': '15px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'maxWidth': '600px',
            'margin': '0 auto'
        }, children=[
            html.H3("📍 Détails ESG de la zone sélectionnée", style={
                'color': '#3B7A57',
                'textAlign': 'center'
            }),
            html.Div(id='esg-details', style={'fontSize': '16px', 'paddingTop': '10px'})
        ])
    ]),

    html.Br(),
    html.Div(style={
        'textAlign': 'center',
        'marginTop': '30px'
    }, children=[
        html.Label("🔍 Filtrer par ville :", style={
            'fontWeight': 'bold',
            'fontSize': '18px'
        }),
        dcc.Dropdown(
            id='ville-dropdown',
            options=[{'label': ville, 'value': ville} for ville in sorted(df['Ville'].unique())],
            placeholder="Sélectionner une ville",
            style={'width': '300px', 'margin': '10px auto'}
        ),
        html.Button("🔄 Réinitialiser", id='reset-button', n_clicks=0, style={
            'marginLeft': '10px',
            'backgroundColor': '#3B7A57',
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'borderRadius': '5px',
            'cursor': 'pointer'
        })
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
    if triggered_id == 'reset-button':
        filtered_df = df
    else:
        filtered_df = df if not selected_ville else df[df['Ville'] == selected_ville]

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
        paper_bgcolor='#F4F9F4'
    )
    return fig

# Callback pour les détails
@app.callback(
    Output('esg-details', 'children'),
    Input('map', 'clickData')
)
def update_dashboard(clickData):
    if clickData:
        zone = clickData['points'][0]['customdata'][0]
        row = df[df['Zone'] == zone].iloc[0]
        return html.Ul([
            html.Li(f"Ville : {row['Ville']}"),
            html.Li(f"Score ESG : {row['Score_ESG']} / 100"),
            html.Li(f"Qualité de l'air : {row['Qualite_Air']}"),
            html.Li(f"Végétalisation : {row['Vegetalisation_%']}%"),
            html.Li(f"Taux de recyclage : {row['Recyclage_%']}%"),
            html.Li(f"Pollution sonore : {row['Pollution_Sonore_dB']} dB"),
            html.Li(f"Accès à la nature : {row['Acces_Nature_m']} m")
        ])
    else:
        return "Cliquez sur une zone de la carte."

if __name__ == '__main__':
    app.run(debug=True)

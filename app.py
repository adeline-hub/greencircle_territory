#1. App Setup & Data

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, ctx
import plotly.graph_objects as go

# Define your custom colorscale or use 'Greens'
custom_scale = [
    [0, '#e0fff9'],
    [1, '#33FFA2']
]

# Charger les données simulées
df = pd.read_csv('esg_simule.csv')

legend_fig = go.Figure(go.Scatter(
    x=[None], y=[None],
    mode='markers',
    marker=dict(
        colorscale=custom_scale,  # Fix here
        showscale=True,
        cmin=df['Score_ESG'].min(),
        cmax=df['Score_ESG'].max(),
        colorbar=dict(
            #orientation='h',
            thickness=20,
            x=0,
            y=0,
            len=1,
            title='Score ESG',
            title_side='top',
            tickfont=dict(color='#2F4F4F')
        )
    ),
    hoverinfo='skip'
))


legend_fig.update_layout(
    width=600,
    height=80,
    margin=dict(l=0, r=0, t=20, b=0),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
)



# Initialiser l'app Dash
app = Dash(__name__)
server = app.server  # Pour Render


#2.  App Layout

app.title = "GreenCircle ESG Prototype"

app.layout = html.Div(style={
    'fontFamily': 'Courier New',
    'backgroundColor': 'oldlace',
    'padding': '20px'
}, children=[

    # Header Section
    
    html.H1("GreenCircle scoring ESG in city", style={
        'color': '#313130',
        'textAlign': 'center',
        'fontSize': '36px',
        'marginBottom': '30px'
    }),
    
    # Add the shared colorbar legend here
    html.Div([
        dcc.Graph(
            figure=legend_fig,
            config={'displayModeBar': False},
            style={'height': '80px', 'width': '100%'}
        )
    ], style={'marginBottom': '30px'}),
    
    html.P(
    "GreenCircle embraces a city-focused approach to sustainable development, acknowledging the pivotal and integrative role that cities and urban life play in advancing sustainability.",
    style={'color': '#333', 'fontSize': '16px', 'textAlign': 'center', 'marginBottom': '20px'}
),

    
    html.Div([
        html.Label("Filter by city:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='ville-dropdown',
            options=[{'label': ville, 'value': ville} for ville in sorted(df['Ville'].unique())],
            placeholder="Select a city",
            style={'width': '300px', 'marginBottom': '10px'}
        ),
        html.Button("🔄 Reset", id='reset-button', n_clicks=0, style={'marginLeft': '10px'})
    ]),

    html.Div(style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'space-between',
        'marginTop': '20px'
    }, children=[

        # ESG map
        html.Div(style={
            'flex': '1',
            'minWidth': '40%',
            'height': '70vh',
            'marginRight': '20px',
            'backgroundColor': '#313130',
            'borderRadius': '15px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'padding': '10px'
        }, children=[
            html.H3("ESG map", style={'textAlign': 'center', 'color': 'oldlace'}),
            dcc.Graph(id='map', style={
                'height': '60vh'
            })
        ]),
        #
        #
        html.Div(style={
            'flex': '1',
            'minWidth': '40%',
            'height': '70vh',
            'backgroundColor': '#313130',
            'borderRadius': '15px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'padding': '10px'
        }, children=[
            html.H3("Top 10 ESG cities", style={
                'textAlign': 'center',
                'color': 'oldlace'
            }),
            dcc.Graph(id='bar-chart', style={
                'height': '60vh'
            })
        ])
    ]),
    
html.P(
    "A smart sustainable city is an innovative city that uses ICTs and other means to improve quality of life, efficiency of urban operation and services, and competitiveness, while ensuring that it meets the needs of present and future generations with respect to economic, social, environmental as well as cultural aspects. "
    "UNECE standard on Smart Sustainable Cities",
    style={'color': '#333', 'fontSize': '16px', 'textAlign': 'center', 'marginBottom': '20px'}
),

    html.Div(style={
        'marginTop': '30px',
        'backgroundColor': '#313130',
        'borderRadius': '15px',
        'padding': '20px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
    }, children=[
        html.H3("Correlation between Greening and Recycling", style={
            'textAlign': 'center',
            'color': 'oldlace'
        }),
        dcc.Graph(id='scatter-plot')
    ])
    
])

#  3. Callbacks (Logic & Interactivity)



# Map Callback pour la carte
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
        height=500,
        color_continuous_scale= custom_scale
    )
    fig.update_traces(marker_showscale=False)
    fig.update_layout(
        coloraxis_showscale=False, mapbox_style="carto-positron",
        font=dict(color='oldlace', family='Courier New', size=14),
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
        color_continuous_scale= custom_scale
    )
    fig.update_traces(marker_showscale=False)
    fig.update_layout(bargap=0.5,coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'}, height=500, font=dict(color='oldlace', family='Courier New', size=14),margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
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
        color='Score_ESG',   # numeric for continuous scale
        hover_name='Zone',
        size='Score_ESG',
        title='Greening vs Recycling',
        color_continuous_scale=custom_scale,
        height=500
    )
    fig.update_traces(marker_showscale=False)
    fig.update_layout(coloraxis_showscale=False,title_font=dict(color='oldlace'), font=dict(color='oldlace', family='Courier New', size=14), margin=dict(l=0, r=0, t=40, b=0), paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig

if __name__ == '__main__':
    app.run(debug=True)




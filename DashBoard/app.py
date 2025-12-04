# dashboard/app.py
import pandas as pd
import plotly.express as px
import webbrowser
from threading import Timer
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# load data (path relative to dashboard folder)
df = pd.read_excel("cleaned_weather.xls")


df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')

app = Dash(__name__)
server = app.server

# layout
app.layout = html.Div([
    html.H2("ClimateScope — Interactive Dashboard", style={'textAlign':'center'}),
    html.Div([
        dcc.Dropdown(
            id='country_dropdown',
            options=[{'label': c, 'value': c} for c in sorted(df['country'].unique())],
            value=df['country'].unique()[0],
            clearable=False,
            style={'width':'50%'}
        )
    ], style={'textAlign':'center', 'padding':'10px'}),

    dcc.Graph(id='temp_trend'),
    html.Hr(),
    dcc.Graph(
        id='world_map',
        figure=px.choropleth(
            df.groupby('country', as_index=False).mean(numeric_only=True),
            locations='country',
            locationmode='country names',
            color='temperature_celsius',
            title='Average Temperature by Country',
            color_continuous_scale='thermal'
        )
    )
], style={'maxWidth':'1200px', 'margin':'auto'})

# callbacks
@app.callback(
    Output('temp_trend', 'figure'),
    [Input('country_dropdown', 'value')]
)
def update_temp_trend(country):
    sub = df[df['country'] == country].sort_values('last_updated')
    if sub.empty:
        return px.line(title=f"No data for {country}")
    fig = px.line(sub, x='last_updated', y='temperature_celsius',
                  title=f'Temperature Trend — {country}', markers=True)
    fig.update_layout(yaxis_title='Temperature (°C)')
    return fig

# open browser automatically
def open_browser():
    webbrowser.open("http://127.0.0.1:8050/", new=2)

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=False, host='127.0.0.1', port=8050)

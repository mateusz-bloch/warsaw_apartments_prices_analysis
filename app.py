from dash import Dash, dcc, html, Input, Output
from datetime import date
from datetime import timedelta
from app_script.warsaw_chart import *

app = Dash(__name__)

start_date = date(2022, 11, 15) 
actual_date = date.today()   
delta = actual_date - start_date   
days = []

for i in range(delta.days + 1):
    days.append(str(start_date + timedelta(days=i)))

app.layout = html.Div([
    html.H1('Warsaw apartment prices '),
    dcc.Dropdown(days, str(days[-1]), id='date_dropdown'),
    html.Div([
        html.Div([
            html.H2('Price of Apartaments'),
            dcc.Graph(
            id='choro_cena',
            className='chart'
        )
        ]),
        html.Div([
            html.H2('Price of Apartaments per m2'),
            dcc.Graph(
            id='choro_cena_za_metr',
            className='chart'
        )
        ]),
        html.Div([
            html.H2('Apartments area'),
            dcc.Graph(
            id='choro_metraz',
            className='chart'
        )
        ])
    ], className='container'),
    html.Div([
        html.Div([
            html.H2('Price of Apartaments'),
            dcc.Graph(
            id='hist_cena',
            className='chart'
        )
        ]),
        html.Div([
            html.H2('Price of Apartaments per m2'),
            dcc.Graph(
            id='hist_cena_za_metr',
            className='chart'
        )
        ]),
        html.Div([
            html.H2('Apartments area'),
            dcc.Graph(
            id='hist_metraz',
            className='chart'
        )
        ])
    ], className='container'),
    html.Div([
        html.Div([
            html.H2('Price of Apartaments'),
            dcc.Graph(
            id='scatter_diag',
            className='chart_full'
        )
        ])
    ], className='container'),
    html.Div([
        html.Div([
            html.H2('Price of Apartaments'),
            dcc.Graph(
            id='density_diag',
            className='chart_full'
        )
        ])
    ], className='container')

])

@app.callback(
    Output('choro_cena', 'figure'),
    Output('choro_cena_za_metr', 'figure'),
    Output('choro_metraz', 'figure'),
    Output('hist_cena', 'figure'),
    Output('hist_cena_za_metr', 'figure'),
    Output('hist_metraz', 'figure'),
    Output('scatter_diag', 'figure'),
    Output('density_diag', 'figure'),
    Input('date_dropdown', 'value'))
def update_figure(date_dropdown):
    choro_cena = warsaw_choro('Price in PLN', date_dropdown)
    choro_cena_za_metr = warsaw_choro('Price per meter', date_dropdown)
    choro_metraz = warsaw_choro('Apartment area', date_dropdown)
    hist_cena = warsaw_hist('Price in PLN', date_dropdown)
    hist_cena_za_metr = warsaw_hist('Price per meter', date_dropdown)
    hist_metraz = warsaw_hist('Apartment area', date_dropdown)
    scatter_diag = warsaw_scatter(date_dropdown)
    density_diag = warsaw_density(date_dropdown)
    return choro_cena, choro_cena_za_metr, choro_metraz, hist_cena, hist_cena_za_metr, hist_metraz, scatter_diag, density_diag

if __name__ == '__main__':
    app.run_server(debug=True)
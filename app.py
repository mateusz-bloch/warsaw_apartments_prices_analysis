from dash import Dash, dcc, html, Input, Output
from datetime import date
from datetime import timedelta
from app_script.warsaw_chart import *
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

start_date = date(2022, 11, 15) 
actual_date = date.today()   
delta = actual_date - start_date   
days = []
districts = ["Bemowo", "Białołęka", "Bielany", "Mokotów", "Ochota", "Praga Południe", "Praga Północ", "Rembertów", "Targówek", "Ursus", "Ursynów", "Wawer", "Wesoła", "Wilanów", "Wola", "Włochy", "Śródmieście", "Żoliborz"]

for i in range(delta.days + 1):
    days.append(str(start_date + timedelta(days=i)))

app.layout = html.Div([
    html.H1('Warsaw apartment prices '),
    dcc.Dropdown(days, str(days[-1]), id='date_dropdown', className='dropdown_class'),
    dbc.Row([
        dbc.Col([
            html.H3('Average price of apartaments'),
            html.H6('   Description'),
            dcc.Graph(
            id='choro_cena'
        )
        ], width=3),
        dbc.Col([
            html.H3('Average price of apartaments per m2'),
            dcc.Graph(
            id='choro_cena_za_metr'
        )
        ], width=3),
        dbc.Col([
            html.H3('Average apartments area'),
            dcc.Graph(
            id='choro_metraz'
        )
        ], width=3)
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            html.H3('Price of Apartaments by the number of advertisements'),
            dcc.Graph(
            id='hist_cena'
        )
        ], width=3),
        dbc.Col([
            html.H3('Price of Apartaments per m2 by the number of advertisements'),
            dcc.Graph(
            id='hist_cena_za_metr'
        )
        ], width=3),
        dbc.Col([
            html.H3('Apartments area by the number of advertisements'),
            dcc.Graph(
            id='hist_metraz'
        )
        ], width=3)
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            html.H3('The ratio of the price per meter to the area of the apartment'),
            dcc.Graph(
            id='scatter_diag'
        )
        ], width=5),
        dbc.Col([
            html.H3('Price per apartment relative to the district'),
            dcc.Graph(
            id='density_diag'
        )
        ], width=3)
    ], justify="center"),
    html.H2('You can choose the district: '),
    dcc.Dropdown(districts, str(districts[0]), id='district_dropdown', className='dropdown_class'),
        dbc.Row([
        dbc.Col([
            html.H3('Price of Apartaments by the number of advertisements'),
            dcc.Graph(
            id='hist_cena_district'
        )
        ], width=3),
        dbc.Col([
            html.H3('Price of Apartaments per m2 by the number of advertisements'),
            dcc.Graph(
            id='hist_cena_za_metr_district'
        )
        ], width=3),
        dbc.Col([
            html.H3('Apartments area by the number of advertisements'),
            dcc.Graph(
            id='hist_metraz_district'
        )
        ], width=3)
    ], justify="center"),

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

@app.callback(
    Output('hist_cena_district', 'figure'),
    Output('hist_cena_za_metr_district', 'figure'),
    Output('hist_metraz_district', 'figure'),
    Input('district_dropdown', 'value'))
def update_figure(district_dropdown):
    hist_cena_distric = district_hist('Price in PLN', district_dropdown)
    hist_cena_za_metr_district = district_hist('Price per meter', district_dropdown)
    hist_metraz_district = district_hist('Apartment area', district_dropdown)
    return hist_cena_distric, hist_cena_za_metr_district, hist_metraz_district

if __name__ == '__main__':
    app.run_server(debug=True)